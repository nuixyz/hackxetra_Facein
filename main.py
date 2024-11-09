import cv2
import numpy as np
import pickle
import base64
from pymongo import MongoClient
from datetime import datetime
import face_recognition
import time

#duration for class
duration = 10

#make a reload function for easier db refresh

# MongoDB setup
client = MongoClient("mongodb+srv://nuix:ymAmHW2Rdw2CgZAR@cluster0.vpcby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyFirstDatabase"]
collection = db["posts"]

# Load known face encodings from EncodedFile.p
file = open('EncodedFile.p', 'rb')
encodedList, studentIds = pickle.load(file)
file.close()

# Load encodings and names from MongoDB
def load_known_faces_from_mongodb():
    mongo_encodings = []
    mongo_names = []

    for document in collection.find():
        img_data = base64.b64decode(document["image"])
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        encodings = face_recognition.face_encodings(img)
        if encodings:
            mongo_encodings.append(encodings[0])
            mongo_names.append(document["username"])

    return mongo_encodings, mongo_names

mongo_encodings, mongo_names = load_known_faces_from_mongodb()
encodedList.extend(mongo_encodings)
studentIds.extend(mongo_names)

# Set up webcam
cap = cv2.VideoCapture(1)  # Adjust index if needed

# Verify if webcam opens correctly
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

cap.set(3, 1280)
cap.set(4, 720)

start_time = time.time()

while time.time() - start_time < duration:
# while True:
    ret, fframe = cap.read()

    if not ret:
        print("Failed to capture image. Exiting...")
        break

    frame = cv2.flip(fframe, 1)

    resizedImage = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)

    faceLocations = face_recognition.face_locations(resizedImage)
    encodeFrame = face_recognition.face_encodings(resizedImage, faceLocations)

    for encodeFace, faceLocation in zip(encodeFrame, faceLocations):
        matches = face_recognition.compare_faces(encodedList, encodeFace)
        faceDistance = face_recognition.face_distance(encodedList, encodeFace)
        matchIndex = np.argmin(faceDistance)
        confidence = round(100 - np.min(faceDistance) * 100)

        if matches[matchIndex]:
            studentName = studentIds[matchIndex]
            print("Face Detected at index ", matchIndex)
            print("User seems to be", studentName)

            # Update the database to mark the user as present
            collection.update_one(
                {"username": studentName},
                {"$set": {
                    "status": "present",
                    "last_seen": datetime.now()
                }}
            )
            print(f"Marked {studentName} as present in MongoDB.")

            # Draw a rectangle around the matched face
            top, right, bottom, left = faceLocation
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, studentName, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, f"{confidence}%", (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    cv2.imshow("Webcam Face Verification", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Your time is up lil meow meow")
my_query = {"status":"present"}

for x in collection.find(my_query):
    dp = x['days present']
    updated = {"$set":{"days present": dp + 1}}
    collection.update_one(my_query,updated)

tc = x['total classes']
updated = {"$set": {"total classes": tc + 1}}
collection.update_many({}, updated)

# updt = {"total classes":{"$gt": 0}}

# for y in collection.find(updt):
#     print("Im inside the loop")
#     dp = y['days present']
#     tc = y['total classes']
#     updated2 = {"$set":{"attendance percentage": 69}}
#     collection.update_one(y,updated2)

collection.update_many(
  {},
  {"$set": {
    "status": "absent"
  }}
  )


cap.release()
cv2.destroyAllWindows()
