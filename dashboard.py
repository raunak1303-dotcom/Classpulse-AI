import tkinter as tk
import subprocess
import sqlite3
from tkinter import ttk

def get_stats():
    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    conn.close()
    return total_students, total_attendance

def start_attendance():
    subprocess.run(["python", "attendance_system.py"])

def register_student():
    subprocess.run(["python", "register_student.py"])
    subprocess.run(["python", "train_model.py"])

def view_attendance():
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    records_window.geometry("750x400")
    records_window.configure(bg="#111827")

    tree = ttk.Treeview(
        records_window,
        columns=("ID", "Name", "Date", "Time"),
        show="headings"
    )

    for col in ("ID", "Name", "Date", "Time"):
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")

    for record in cursor.fetchall():
        tree.insert("", tk.END, values=record)

    conn.close()

def view_students():
    students_window = tk.Toplevel(root)
    students_window.title("Registered Students")
    students_window.geometry("850x400")
    students_window.configure(bg="#111827")

    tree = ttk.Treeview(
        students_window,
        columns=("ID", "Name", "Roll No", "Class", "Phone"),
        show="headings"
    )

    for col in ("ID", "Name", "Roll No", "Class", "Phone"):
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")

    for student in cursor.fetchall():
        tree.insert("", tk.END, values=student)

    conn.close()

root = tk.Tk()
root.title("ClassPulse AI Dashboard")
root.geometry("760x760")
root.configure(bg="#0f172a")

title = tk.Label(
    root,
    text="ClassPulse AI",
    font=("Segoe UI", 32, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)
title.pack(pady=(30, 5))

tagline = tk.Label(
    root,
    text="Capturing the Pulse of Every Classroom",
    font=("Segoe UI", 13),
    bg="#0f172a",
    fg="#cbd5e1"
)
tagline.pack(pady=(0, 20))

total_students, total_attendance = get_stats()

stats_frame = tk.Frame(root, bg="#0f172a")
stats_frame.pack(pady=15)

student_card = tk.Label(
    stats_frame,
    text=f"👥 Total Students\n{total_students}",
    font=("Segoe UI", 15, "bold"),
    bg="#1e293b",
    fg="white",
    width=18,
    height=4
)
student_card.grid(row=0, column=0, padx=15)

attendance_card = tk.Label(
    stats_frame,
    text=f"✅ Attendance Records\n{total_attendance}",
    font=("Segoe UI", 15, "bold"),
    bg="#1e293b",
    fg="white",
    width=22,
    height=4
)
attendance_card.grid(row=0, column=1, padx=15)

card = tk.Frame(root, bg="#1e293b", padx=40, pady=30)
card.pack(pady=20)

def styled_button(text, command, color):
    return tk.Button(
        card,
        text=text,
        font=("Segoe UI", 14, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        width=28,
        height=2,
        bd=0,
        cursor="hand2",
        command=command
    )

styled_button("Register Student", register_student, "#2563eb").pack(pady=10)
styled_button("Start Attendance System", start_attendance, "#16a34a").pack(pady=10)
styled_button("View Attendance", view_attendance, "#9333ea").pack(pady=10)
styled_button("View Students", view_students, "#ea580c").pack(pady=10)
styled_button("Exit", root.quit, "#dc2626").pack(pady=10)

footer = tk.Label(
    root,
    text="AI Powered Attendance • Face Recognition • Smart Classroom Analytics",
    font=("Segoe UI", 10),
    bg="#0f172a",
    fg="#94a3b8"
)
footer.pack(side="bottom", pady=15)

root.mainloop()