import cv2
import os

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Create students folder
if not os.path.exists("students"):
    os.makedirs("students")

name = input("Enter student name: ")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    # Draw rectangle around face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

        # Crop only face
        face_crop = frame[y:y+h, x:x+w]

    cv2.putText(
        frame,
        "Press S to save face",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.imshow("ClassPulse AI Registration", frame)

    key = cv2.waitKey(1)

    # Save cropped face
    if key == ord('s'):

        if len(faces) > 0:
            filename = f"students/{name}.jpg"
            cv2.imwrite(filename, face_crop)

            print(f"{name} registered successfully!")
            print("Face image saved.")

            break

        else:
            print("No face detected!")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()