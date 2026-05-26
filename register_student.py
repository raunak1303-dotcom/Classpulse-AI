import cv2
import os
import sqlite3

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if not os.path.exists("students"):
    os.makedirs("students")

name = input("Enter student name: ")
roll_no = input("Enter roll number: ")
class_name = input("Enter class/section: ")
phone = input("Enter phone number: ")

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

cap = cv2.VideoCapture(0)
face_crop = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        face_crop = frame[y:y+h, x:x+w]

    cv2.putText(frame, "Press S to save | Q to quit", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Register Student", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        if face_crop is not None:
            filename = f"students/{roll_no}_{name}.jpg"
            cv2.imwrite(filename, face_crop)

            try:
                cursor.execute("""
                INSERT INTO students (name, roll_no, class_name, phone)
                VALUES (?, ?, ?, ?)
                """, (name, roll_no, class_name, phone))

                conn.commit()
                print(f"{name} registered successfully!")

            except sqlite3.IntegrityError:
                print("Roll number already exists!")

            break
        else:
            print("No face detected!")

    elif key == ord('q'):
        break

cap.release()
conn.close()
cv2.destroyAllWindows()