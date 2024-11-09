import cv2
import os

cap = cv2.VideoCapture(1)

username = input("Please state your name: ")

while True:
    check, frame = cap.read()
    print(check)
    print(frame)
    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(32)
    if key == ord(" "): 
        path = 'photos'
        filename = f"{username}.jpg"
        
        # Save the captured frame
        cv2.imwrite(os.path.join(path, filename), frame)
        cap.release()
        
        # Reload and display the saved image
        img_new = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
        cv2.imshow("Captured Image", img_new)
        cv2.waitKey(1650)
        cv2.destroyAllWindows() 
        break
    
    elif key == ord('q'):
        print("Turning off camera.")
        cap.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
