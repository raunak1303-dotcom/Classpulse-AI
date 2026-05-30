import cv2
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if not os.path.exists("students"):
    os.makedirs("students")


def capture_face(name, roll_no, class_name, phone):
    if not name or not roll_no or not class_name:
        messagebox.showerror("Error", "Name, Roll No and Class are required.")
        return

    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()

    cap = cv2.VideoCapture(0)
    face_crop = None

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

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_crop = frame[y:y+h, x:x+w]

        cv2.putText(
            frame,
            "Press S to Save | Q to Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("ClassPulse AI - Face Capture", frame)

        key = cv2.waitKey(1)

        if key == ord("s"):
            if face_crop is not None:
                filename = f"students/{roll_no}_{name}.jpg"
                cv2.imwrite(filename, face_crop)

                try:
                    cursor.execute("""
                    INSERT INTO students (name, roll_no, class_name, phone)
                    VALUES (?, ?, ?, ?)
                    """, (name, roll_no, class_name, phone))

                    conn.commit()

                    messagebox.showinfo(
                        "Success",
                        f"{name} registered successfully!\nNow training model..."
                    )

                    os.system("python train_model.py")

                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Roll number already exists.")

                break

            else:
                messagebox.showerror("Error", "No face detected.")

        elif key == ord("q"):
            break

    cap.release()
    conn.close()
    cv2.destroyAllWindows()


def register():
    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    class_name = class_entry.get().strip()
    phone = phone_entry.get().strip()

    capture_face(name, roll_no, class_name, phone)


root = tk.Tk()
root.title("ClassPulse AI - Student Registration")
root.geometry("600x550")
root.configure(bg="#0b1120")

tk.Label(
    root,
    text="Student Registration",
    font=("Segoe UI", 28, "bold"),
    bg="#0b1120",
    fg="#38bdf8"
).pack(pady=(40, 10))

tk.Label(
    root,
    text="Enter details and capture face for ClassPulse AI",
    font=("Segoe UI", 12),
    bg="#0b1120",
    fg="#94a3b8"
).pack(pady=(0, 30))

form = tk.Frame(root, bg="#1e293b", padx=40, pady=30)
form.pack()

def label(text):
    return tk.Label(
        form,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bg="#1e293b",
        fg="white",
        anchor="w"
    )

def entry():
    return tk.Entry(
        form,
        font=("Segoe UI", 12),
        width=32
    )

label("Name").pack(anchor="w", pady=(0, 5))
name_entry = entry()
name_entry.pack(pady=(0, 15))

label("Roll Number").pack(anchor="w", pady=(0, 5))
roll_entry = entry()
roll_entry.pack(pady=(0, 15))

label("Class / Section").pack(anchor="w", pady=(0, 5))
class_entry = entry()
class_entry.pack(pady=(0, 15))

label("Phone Number").pack(anchor="w", pady=(0, 5))
phone_entry = entry()
phone_entry.pack(pady=(0, 25))

tk.Button(
    form,
    text="Capture Face & Register",
    font=("Segoe UI", 13, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=register
).pack(pady=10)

tk.Button(
    root,
    text="Close",
    font=("Segoe UI", 11, "bold"),
    bg="#dc2626",
    fg="white",
    width=14,
    height=1,
    bd=0,
    cursor="hand2",
    command=root.destroy
).pack(pady=25)

root.mainloop()