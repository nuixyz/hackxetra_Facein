import os
import cv2
import face_recognition
import pickle

imageFolderPath= 'chayans-tests/testSubjects'
imagePathList = os.listdir(imageFolderPath)

imageList = []
studentIds = []

for path in imagePathList:
    img_path = os.path.join(imageFolderPath, path)
    img = cv2.imread(img_path)
    
    if img is not None:
        imageList.append(img)
        studentIds.append(os.path.splitext(path)[0])
    else:
        print(f"Failed to load image at path: {img_path}")

print(studentIds)
print(len(imageList))

def encodeGenerator(someImageListHere):
  encodeList = []
  for img in imageList:
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encodes = face_recognition.face_encodings(img)[0]
    encodeList.append(encodes)
  return encodeList

encodedList = encodeGenerator(imageList)
# print(encodedList)
encodedListAndIds = [encodedList, studentIds]

file = open("chayans-tests/EncodedFile.p", 'wb')
pickle.dump(encodedListAndIds, file)
file.close()