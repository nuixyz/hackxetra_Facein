import os
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import threading

directories = ['templates', 'static']

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registration and Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Register</h1>
        <form action="/register" method="post">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Register</button>
        </form>

        <h1>Login</h1>
        <form action="/login" method="post">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>'''

with open('templates/login.html', 'w') as file:
    file.write(html_content)

css_content = '''body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.container {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
    text-align: center;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    text-align: left;
}

input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}'''

with open('static/styles.css', 'w') as file:
    file.write(css_content)


app = Flask(__name__)
app.secret_key = 'supersecretkey'


client = MongoClient("mongodb+srv://nuix:ymAmHW2Rdw2CgZAR@cluster0.vpcby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_registration']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    if users_collection.find_one({'email': email}):
        return 'User already exists!'
    
    hashed_password = generate_password_hash(password)
    user_data = {
        'email': email,
        'password': hashed_password
    }
    users_collection.insert_one(user_data)
    return 'User registered successfully!'

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['_id']
        session['email'] = user['email']
        return 'Login successful!'
    else:
        return 'Invalid email or password. Please try again.'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def run_app():
    app.run()


thread = threading.Thread(target=run_app)
thread.start()