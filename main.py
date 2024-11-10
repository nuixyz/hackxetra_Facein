import cv2
import numpy as np
import pickle
import base64
from pymongo import MongoClient
from datetime import datetime
import face_recognition
import time

# Duration for class
duration = 10

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

# Append MongoDB encodings to the existing list
mongo_encodings, mongo_names = load_known_faces_from_mongodb()
encodedList.extend(mongo_encodings)
studentIds.extend(mongo_names)


cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

frame_count = 0
frame_skip = 5

recognized_users = set()

start_time = time.time()

while time.time() - start_time < duration:
    ret, fframe = cap.read()
    if not ret:
        print("Failed to capture image. Exiting...")
        break

    frame = cv2.flip(fframe, 1)

    # Only process every nth frame
    frame_count += 1
    if frame_count % frame_skip != 0:
        cv2.imshow("Webcam Face Verification", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    resizedImage = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)

    faceLocations = face_recognition.face_locations(resizedImage)
    encodeFrame = face_recognition.face_encodings(resizedImage, faceLocations)

    for encodeFace, faceLocation in zip(encodeFrame, faceLocations):
        matches = face_recognition.compare_faces(encodedList, encodeFace)
        faceDistance = face_recognition.face_distance(encodedList, encodeFace)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex] and faceDistance[matchIndex] < 0.5:
            studentName = studentIds[matchIndex]
            if studentName not in recognized_users:
                recognized_users.add(studentName)
                print(f"{studentName} detected and marked as present.")

                collection.update_one(
                    {"username": studentName},
                    {"$set": {
                        "status": "present",
                        "last_seen": datetime.now()
                    }}
                )

            top, right, bottom, left = faceLocation
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, studentName, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    cv2.imshow("Webcam Face Verification", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Time up!")

#Increment attendance stats after loop ends
for user in recognized_users:
    user_record = collection.find_one({"username": user})
    daysPresent = user_record['days present']
    collection.update_one(
        {"username": user},
        {"$set": {"days present": daysPresent + 1}}
    )

collection.update_many({}, {"$inc": {"total classes": 1}})

# Reset status for next session
collection.update_many({}, {"$set": {"status": "absent"}})

cap.release()
cv2.destroyAllWindows()
