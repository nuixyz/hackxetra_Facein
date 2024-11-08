import cv2
import numpy as np
import pickle
import face_recognition

cap = cv2.VideoCapture(1)
#change the below values to something else, these control the dimensions of the webcam
cap.set(3, 1280)
cap.set(4, 720)

file = open('chayans-tests/EncodedFile.p', 'rb')
encodedListAndIds = pickle.load(file)
file.close()
encodedList, studentIds = encodedListAndIds
print(studentIds)

while True:
  succes, img = cap.read()

  resizedImage = cv2.resize(img, (0,0), None, 0.25, 0.25)
  resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)

  faceFrame = face_recognition.face_locations(resizedImage)
  encodeFrame = face_recognition.face_encodings(resizedImage, faceFrame)

  for encodeFace, faceLocation in zip(encodeFrame, faceFrame):
    matches = face_recognition.compare_faces(encodedList, encodeFace)
    faceDistance = face_recognition.face_distance(encodedList, encodeFace)

    # print("matches", matches)
    # print("faceDistance", faceDistance)

    matchIndex = np.argmin(faceDistance)
    # print("Match Index", matchIndex)
    
    if matches[matchIndex]:
      print("Face Detected at index ", matchIndex)
      print("User seems to be", studentIds[matchIndex])
      # cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
  cv2.imshow("Webcam", img)
  cv2.waitKey(1)