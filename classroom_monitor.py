import cv2
import sqlite3
import time
from datetime import datetime
from ultralytics import YOLO

# ================= DATABASE =================
conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

# ================= MODELS =================
model = YOLO("yolov8n.pt")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

names = {}

with open("names.txt", "r") as f:
    for line in f:
        label, name = line.strip().split(",", 1)
        names[int(label)] = name

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

checked_attendance = set()
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

    # ================= PHONE DETECTION =================
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

    # ================= FACE RECOGNITION =================
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if confidence < 50:
            raw_name = names[label]
        else:
            raw_name = "Unknown"

        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        # Extract clean name and roll number from filename format: roll_name
        if raw_name != "Unknown" and "_" in raw_name:
            extracted_roll, extracted_name = raw_name.split("_", 1)
        else:
            extracted_roll = "N/A"
            extracted_name = raw_name

        display_name = extracted_name if raw_name != "Unknown" else "Unknown"

        if raw_name != "Unknown":

            # ---------- FETCH STUDENT DETAILS ----------
            cursor.execute("""
            SELECT roll_no, class_name
            FROM students
            WHERE roll_no=? OR name=?
            """, (extracted_roll, extracted_name))

            student_data = cursor.fetchone()

            if student_data:
                roll_no, class_name = student_data
            else:
                roll_no, class_name = extracted_roll, "N/A"

            # ---------- MARK ATTENDANCE ----------
            if extracted_name not in checked_attendance:

                cursor.execute("""
                SELECT * FROM attendance
                WHERE name=? AND date=?
                """, (extracted_name, today))

                already_marked = cursor.fetchone()

                if already_marked is None:
                    cursor.execute("""
                    INSERT INTO attendance (name, date, time, roll_no, class_name)
                    VALUES (?, ?, ?, ?, ?)
                    """, (extracted_name, today, current_time, roll_no, class_name))

                    conn.commit()
                    print(f"{extracted_name} attendance marked")

                else:
                    print(f"{extracted_name} already marked today")

                checked_attendance.add(extracted_name)

            # ---------- ENGAGEMENT TRACKING ----------
            if extracted_name not in student_stats:
                student_stats[extracted_name] = {
                    "total_frames": 0,
                    "face_frames": 0,
                    "phone_frames": 0
                }

            student_stats[extracted_name]["total_frames"] += 1
            student_stats[extracted_name]["face_frames"] += 1

            if phone_detected:
                student_stats[extracted_name]["phone_frames"] += 1

        # ---------- DRAW FACE UI ----------
        color = (0, 255, 0) if raw_name != "Unknown" else (0, 255, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(
            frame,
            display_name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    # ================= MAIN SCREEN TITLE =================
    cv2.putText(
        frame,
        "ClassPulse AI - Classroom Monitoring",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # ================= LIVE ALERT SYSTEM =================
    live_attention_score = 100

    if phone_detected:
        live_attention_score -= 40

    if len(faces) == 0:
        live_attention_score -= 30

    live_attention_score = max(0, min(100, live_attention_score))

    # ================= CLASSPULSE METER =================
    bar_x = 20
    bar_y = 80
    bar_width = 300
    bar_height = 30

    filled_width = int((live_attention_score / 100) * bar_width)

    if live_attention_score >= 70:
        meter_color = (0, 200, 0)
    elif live_attention_score >= 40:
        meter_color = (0, 215, 255)
    else:
        meter_color = (0, 0, 255)

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + bar_width, bar_y + bar_height),
        (50, 50, 50),
        -1
    )

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + filled_width, bar_y + bar_height),
        meter_color,
        -1
    )

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + bar_width, bar_y + bar_height),
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"ClassPulse: {live_attention_score}%",
        (bar_x, bar_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("ClassPulse AI - Classroom Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ================= SESSION END REPORT =================
end_time = time.time()
session_duration = end_time - start_time
today = datetime.now().strftime("%Y-%m-%d")

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