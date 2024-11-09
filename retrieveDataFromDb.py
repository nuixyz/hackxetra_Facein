from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb+srv://nuix:ymAmHW2Rdw2CgZAR@cluster0.vpcby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyFirstDatabase"]
collection = db["posts"]

# Retrieve all documents from the collection
documents = collection.find()

# Print each document
for document in documents:
    img_data = base64.b64decode(document["image"])
    img_array = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
