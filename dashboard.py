import tkinter as tk
import subprocess
import sqlite3
from tkinter import ttk, messagebox
from openpyxl import Workbook


def get_stats():
    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    conn.close()
    return total_students, total_attendance


def start_classroom_monitoring():
    subprocess.run(["python", "classroom_monitor.py"])


def register_student():
    subprocess.run(["python", "register_student.py"])
    subprocess.run(["python", "train_model.py"])


def export_attendance():
    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, roll_no, class_name, date, time
    FROM attendance
    """)

    records = cursor.fetchall()
    conn.close()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Attendance Report"

    sheet.append(["ID", "Name", "Roll No", "Class", "Date", "Time"])

    for record in records:
        sheet.append(record)

    workbook.save("attendance_report.xlsx")

    messagebox.showinfo(
        "Export Successful",
        "Attendance report exported as attendance_report.xlsx"
    )


def view_attendance():
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    records_window.geometry("950x500")
    records_window.configure(bg="#111827")

    search_frame = tk.Frame(records_window, bg="#111827")
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search:",
        font=("Segoe UI", 12, "bold"),
        bg="#111827",
        fg="white"
    ).grid(row=0, column=0, padx=10)

    search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=35)
    search_entry.grid(row=0, column=1, padx=10)

    tree = ttk.Treeview(
        records_window,
        columns=("ID", "Name", "Roll No", "Class", "Date", "Time"),
        show="headings"
    )

    for col in ("ID", "Name", "Roll No", "Class", "Date", "Time"):
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    def load_records(keyword=""):
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect("classpulse.db")
        cursor = conn.cursor()

        if keyword == "":
            cursor.execute("""
            SELECT id, name, roll_no, class_name, date, time
            FROM attendance
            """)
        else:
            cursor.execute("""
            SELECT id, name, roll_no, class_name, date, time
            FROM attendance
            WHERE name LIKE ?
            OR roll_no LIKE ?
            OR class_name LIKE ?
            OR date LIKE ?
            """, (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            ))

        for record in cursor.fetchall():
            tree.insert("", tk.END, values=record)

        conn.close()

    tk.Button(
        search_frame,
        text="Search",
        font=("Segoe UI", 11, "bold"),
        bg="#2563eb",
        fg="white",
        padx=15,
        command=lambda: load_records(search_entry.get())
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        search_frame,
        text="Reset",
        font=("Segoe UI", 11, "bold"),
        bg="#dc2626",
        fg="white",
        padx=15,
        command=lambda: load_records("")
    ).grid(row=0, column=3, padx=10)

    load_records()


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


def view_engagement():
    engagement_window = tk.Toplevel(root)
    engagement_window.title("Engagement Reports")
    engagement_window.geometry("1100x500")
    engagement_window.configure(bg="#111827")

    tree = ttk.Treeview(
        engagement_window,
        columns=(
            "ID",
            "Name",
            "Date",
            "Duration",
            "Face Presence",
            "Phone Usage",
            "Attention Score",
            "Status"
        ),
        show="headings"
    )

    for col in (
        "ID",
        "Name",
        "Date",
        "Duration",
        "Face Presence",
        "Phone Usage",
        "Attention Score",
        "Status"
    ):
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = sqlite3.connect("classpulse.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, date, session_duration, face_presence, phone_usage, attention_score, status
    FROM engagement
    """)

    for record in cursor.fetchall():
        tree.insert("", tk.END, values=record)

    conn.close()


root = tk.Tk()
root.title("ClassPulse AI Dashboard")
root.geometry("1200x900")
root.configure(bg="#0f172a")

exit_top = tk.Button(
    root,
    text="⏻ Exit",
    font=("Segoe UI", 13, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    width=10,
    height=1,
    bd=0,
    cursor="hand2",
    command=root.quit
)
exit_top.place(x=1060, y=25)

title = tk.Label(
    root,
    text="ClassPulse AI",
    font=("Segoe UI", 34, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)
title.pack(pady=(40, 5))

tagline = tk.Label(
    root,
    text="Capturing the Pulse of Every Classroom",
    font=("Segoe UI", 13),
    bg="#0f172a",
    fg="#cbd5e1"
)
tagline.pack(pady=(0, 25))

total_students, total_attendance = get_stats()

stats_frame = tk.Frame(root, bg="#0f172a")
stats_frame.pack(pady=10)

student_card = tk.Label(
    stats_frame,
    text=f"👥  Total Students\n{total_students}",
    font=("Segoe UI", 15, "bold"),
    bg="#1e293b",
    fg="white",
    width=20,
    height=4
)
student_card.grid(row=0, column=0, padx=20)

attendance_card = tk.Label(
    stats_frame,
    text=f"☑  Attendance Records\n{total_attendance}",
    font=("Segoe UI", 15, "bold"),
    bg="#1e293b",
    fg="white",
    width=24,
    height=4
)
attendance_card.grid(row=0, column=1, padx=20)

card = tk.Frame(root, bg="#1e293b", padx=45, pady=25)
card.pack(pady=25)


def styled_button(text, command, color):
    return tk.Button(
        card,
        text=text,
        font=("Segoe UI", 13, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        width=38,
        height=2,
        bd=0,
        cursor="hand2",
        command=command
    )


styled_button("👤➕  Register Student", register_student, "#2563eb").pack(pady=7)
styled_button("🧠  Start Classroom Monitoring", start_classroom_monitoring, "#16a34a").pack(pady=9)
styled_button("📋  View Attendance", view_attendance, "#9333ea").pack(pady=7)
styled_button("👥  View Students", view_students, "#ea580c").pack(pady=7)
styled_button("📈  View Engagement Reports", view_engagement, "#0f766e").pack(pady=7)
styled_button("📊  Export Attendance", export_attendance, "#0891b2").pack(pady=7)

footer = tk.Label(
    root,
    text="AI Powered Attendance  •  Face Recognition  •  Phone Detection  •  Engagement Analytics  •  Smart Classroom Monitoring",
    font=("Segoe UI", 10),
    bg="#0f172a",
    fg="#94a3b8"
)
footer.pack(side="bottom", pady=18)

root.mainloop()