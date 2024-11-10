import os
from flask import Flask, jsonify, request, session
from pymongo import MongoClient
from flask_cors import CORS

# Flask API-only app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for React frontend

# MongoDB connection
mongo_uri = "mongodb+srv://kostov:x63gFRW6XbWfYPU4@cluster0.vpcby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
# db = client['user_registration']
# users_collection = db['users']
db = client["MyFirstDatabase"]
collection = db["posts"]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API"})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = collection.find({}, {"username": 1, "days present": 1, "total classes": 1})
    
    user_list = [{"username": user["username"], "daysPresent": user["days present"], "totalClasses": user["total classes"]} for user in users]
    return jsonify(user_list)



@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'User already exists!'}), 400
    
    hashed_password = generate_password_hash(password)
    user_data = {'email': email, 'password': hashed_password}
    users_collection.insert_one(user_data)
    return jsonify({'message': 'User registered successfully!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])
        session['email'] = user['email']
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully!'})

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
