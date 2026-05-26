import cv2
import sqlite3
from datetime import datetime

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

names = {}

with open("names.txt", "r") as f:
    for line in f:
        label, name = line.strip().split(",")
        names[int(label)] = name

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

checked_students = set()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if confidence < 80:
            name = names[label]

            if name not in checked_students:
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                cursor.execute("""
                SELECT * FROM attendance
                WHERE name=? AND date=?
                """, (name, date))

                result = cursor.fetchone()

                if result is None:
                    cursor.execute("""
                    INSERT INTO attendance (name, date, time)
                    VALUES (?, ?, ?)
                    """, (name, date, time))

                    conn.commit()
                    print(f"{name} attendance stored!")

                else:
                    print(f"{name} already marked today")

                checked_students.add(name)

        else:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow("ClassPulse AI Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
conn.close()
cv2.destroyAllWindows()