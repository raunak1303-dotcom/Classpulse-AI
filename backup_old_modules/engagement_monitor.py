from ultralytics import YOLO
import cv2
import time

# Load YOLO model
model = YOLO("yolov8n.pt")

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

total_frames = 0
face_present_frames = 0
phone_detected_frames = 0

start_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    total_frames += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    face_detected = len(faces) > 0

    if face_detected:
        face_present_frames += 1

    phone_detected = False

    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls]

            if label == "cell phone" and confidence > 0.5:
                phone_detected = True
                phone_detected_frames += 1

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
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if total_frames > 0:
        face_presence_percent = (face_present_frames / total_frames) * 100
        phone_usage_percent = (phone_detected_frames / total_frames) * 100

        attention_score = face_presence_percent - phone_usage_percent
        attention_score = max(0, min(100, attention_score))
    else:
        attention_score = 0

    cv2.putText(
        frame,
        f"Attention Score: {attention_score:.2f}%",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Phone Usage: {phone_usage_percent:.2f}%",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.imshow("ClassPulse AI - Engagement Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

end_time = time.time()
duration = end_time - start_time

cap.release()
cv2.destroyAllWindows()

print("\n===== CLASS ENGAGEMENT REPORT =====")
print(f"Session Duration: {duration:.2f} seconds")
print(f"Total Frames: {total_frames}")
print(f"Face Presence: {face_presence_percent:.2f}%")
print(f"Phone Usage: {phone_usage_percent:.2f}%")
print(f"Final Attention Score: {attention_score:.2f}%")

if attention_score < 50:
    print("ALERT: Low engagement detected.")
else:
    print("Engagement level acceptable.")