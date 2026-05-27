import cv2
import sqlite3
import time
from datetime import datetime
from ultralytics import YOLO

# Database connection
conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

# Load names
names = {}

with open("names.txt", "r") as f:
    for line in f:
        label, name = line.strip().split(",", 1)
        names[int(label)] = name

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

student_stats = {}

start_time = time.time()

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

    # YOLO phone detection
    phone_detected = False
    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls]

            if label == "cell phone" and confidence > 0.5:
                phone_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(
                    frame,
                    "PHONE DETECTED",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if confidence < 50:
            name = names[label]
        else:
            name = "Unknown"

        if name != "Unknown":
            if name not in student_stats:
                student_stats[name] = {
                    "total_frames": 0,
                    "face_frames": 0,
                    "phone_frames": 0
                }

            student_stats[name]["total_frames"] += 1
            student_stats[name]["face_frames"] += 1

            if phone_detected:
                student_stats[name]["phone_frames"] += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("ClassPulse AI - Student Engagement Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

end_time = time.time()
session_duration = end_time - start_time

today = datetime.now().strftime("%Y-%m-%d")

print("\n===== STUDENT ENGAGEMENT REPORT =====\n")

for name, stats in student_stats.items():
    total = stats["total_frames"]
    face_frames = stats["face_frames"]
    phone_frames = stats["phone_frames"]

    face_presence = (face_frames / total) * 100 if total > 0 else 0
    phone_usage = (phone_frames / total) * 100 if total > 0 else 0

    attention_score = face_presence - phone_usage
    attention_score = max(0, min(100, attention_score))

    if attention_score < 50:
        status = "Low Engagement"
    else:
        status = "Acceptable"

    print(f"Student: {name}")
    print(f"Face Presence: {face_presence:.2f}%")
    print(f"Phone Usage: {phone_usage:.2f}%")
    print(f"Attention Score: {attention_score:.2f}%")
    print(f"Status: {status}")
    print("-" * 40)

    cursor.execute("""
    INSERT INTO engagement (
        name, date, session_duration,
        face_presence, phone_usage,
        attention_score, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        today,
        f"{session_duration:.2f} seconds",
        face_presence,
        phone_usage,
        attention_score,
        status
    ))

conn.commit()
conn.close()

cap.release()
cv2.destroyAllWindows()