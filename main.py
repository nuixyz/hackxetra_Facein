import cv2
import numpy as np
import pickle
import face_recognition

cap = cv2.VideoCapture(1)
#change the below values to something else, these control the dimensions of the webcam
cap.set(3, 1280)
cap.set(4, 720)

file = open('EncodedFile.p', 'rb')
encodedListAndIds = pickle.load(file)
file.close()
encodedList, studentIds = encodedListAndIds
print(studentIds)

while True:
  ret, frame = cap.read()

  resizedImage = cv2.resize(frame, (0,0), None, 0.25, 0.25)
  resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)

  faceLocations = face_recognition.face_locations(resizedImage)
  encodeFrame = face_recognition.face_encodings(resizedImage, faceLocations)

  for encodeFace, faceLocation in zip(encodeFrame, faceLocations):
    matches = face_recognition.compare_faces(encodedList, encodeFace)
    faceDistance = face_recognition.face_distance(encodedList, encodeFace) #See how far apart the test image is from the known faces

    # print("matches", matches)
    # print("faceDistance", faceDistance)

    matchIndex = np.argmin(faceDistance)
    # print("Match Index", matchIndex)
    

    # Note: This isn't exactly the same as a "percent match". The scale isn't linear. But you can assume that images with a smaller distance are more similar to each other than ones with a larger distance. 
    #Since I have subtracted it from 100, the opposite should be assumed.
    confidence = round(100-np.min(faceDistance)*100)

    if matches[matchIndex]:
      studentName = studentIds[matchIndex]
      print("Face Detected at index ", matchIndex)
      print("User seems to be", studentName)

      top, right, bottom, left = faceLocation
      top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

      #Draw a rectangle around the matched face
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

      # Add label with student name below the rectangle
      cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(frame, studentName, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
      cv2.putText(frame, str(confidence), (left, bottom + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

  cv2.imshow("Webcam", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break