import cv2
import base64
import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb+srv://nuix:ymAmHW2Rdw2CgZAR@cluster0.vpcby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyFirstDatabase"]
collection = db["posts"]

studentIds = []

def save_images_from_folder(folder_path='Photos'):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Get list of images in the folder
    image_path_list = os.listdir(folder_path)

    # Process and save each image
    for path in image_path_list:
        img_path = os.path.join(folder_path, path)
        img = cv2.imread(img_path)
        
        if img is not None:
            # Extract studentId from the file name
            student_id = os.path.splitext(path)[0]
            studentIds.append(student_id)
            
            # Encode the image as JPEG
            _, buffer = cv2.imencode('.jpg', img)
            # Convert to Base64 string
            image_str = base64.b64encode(buffer).decode('utf-8')
    
            # Create document to insert
            document = {
                "username": student_id,  # Use studentId as username
                "image": image_str,
                "timestamp": datetime.now(),
                "status": "absent",
                "days present": 0,
                "total classes": 0,
                "attendance percentage":0
            }
            
            # Insert document into MongoDB
            collection.insert_one(document)
            print(f"Image '{path}' saved to MongoDB with username '{student_id}'")
    return studentIds

if __name__ == "__main__":
    # Save images from the folder and print each studentId
    student_id_list = save_images_from_folder()
    for name in student_id_list:
        print(name)
