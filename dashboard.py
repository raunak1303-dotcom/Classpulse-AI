import tkinter as tk
import subprocess
import sqlite3
from tkinter import ttk, messagebox
from openpyxl import Workbook


BG = "#0b1120"
CARD = "#1e293b"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
BLUE = "#2563eb"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
ORANGE = "#ea580c"
TEAL = "#0f766e"
CYAN = "#0891b2"
RED = "#dc2626"
DARK = "#111827"


def db_fetch(query, params=()):
    conn = sqlite3.connect("classpulse.db")
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    conn.close()
    return data


def get_stats():
    students = db_fetch("SELECT COUNT(*) FROM students")[0][0]
    attendance = db_fetch("SELECT COUNT(*) FROM attendance")[0][0]
    return students, attendance


def get_analysis_stats():
    avg = db_fetch("SELECT AVG(attention_score) FROM engagement")[0][0] or 0
    sessions = db_fetch("SELECT COUNT(*) FROM engagement")[0][0]
    low = db_fetch("SELECT COUNT(*) FROM engagement WHERE attention_score < 50")[0][0]
    worst = db_fetch("SELECT name FROM engagement ORDER BY attention_score ASC LIMIT 1")
    best = db_fetch("SELECT name FROM engagement ORDER BY attention_score DESC LIMIT 1")
    return round(avg, 2), sessions, low, worst[0][0] if worst else "N/A", best[0][0] if best else "N/A"


def run_script(file):
    subprocess.run(["python", file])


def register_student():
    run_script("register_student_gui.py")
    run_script("train_model.py")


def export_attendance():
    records = db_fetch("""
        SELECT id, name, roll_no, class_name, date, time
        FROM attendance
    """)

    wb = Workbook()
    sheet = wb.active
    sheet.title = "Attendance Report"
    sheet.append(["ID", "Name", "Roll No", "Class", "Date", "Time"])

    for row in records:
        sheet.append(row)

    wb.save("attendance_report.xlsx")
    messagebox.showinfo("Export Successful", "attendance_report.xlsx created successfully.")


def table_window(title, columns, query, size="1000x500"):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(size)
    win.configure(bg=DARK)

    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for row in db_fetch(query):
        tree.insert("", tk.END, values=row)


def view_students():
    table_window(
        "Registered Students",
        ("ID", "Name", "Roll No", "Class", "Phone"),
        "SELECT * FROM students",
        "900x450"
    )


def view_engagement():
    table_window(
        "Engagement Reports",
        ("ID", "Name", "Date", "Duration", "Face Presence", "Phone Usage", "Attention Score", "Status"),
        """
        SELECT id, name, date, session_duration, face_presence, phone_usage, attention_score, status
        FROM engagement
        """,
        "1150x520"
    )


def view_attendance():
    win = tk.Toplevel(root)
    win.title("Attendance Records")
    win.geometry("1000x550")
    win.configure(bg=DARK)

    search_frame = tk.Frame(win, bg=DARK)
    search_frame.pack(pady=12)

    tk.Label(search_frame, text="Search:", bg=DARK, fg=TEXT, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=8)

    entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=35)
    entry.grid(row=0, column=1, padx=8)

    cols = ("ID", "Name", "Roll No", "Class", "Date", "Time")
    tree = ttk.Treeview(win, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    def load(keyword=""):
        for row in tree.get_children():
            tree.delete(row)

        if keyword:
            rows = db_fetch("""
                SELECT id, name, roll_no, class_name, date, time
                FROM attendance
                WHERE name LIKE ? OR roll_no LIKE ? OR class_name LIKE ? OR date LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        else:
            rows = db_fetch("""
                SELECT id, name, roll_no, class_name, date, time
                FROM attendance
            """)

        for r in rows:
            tree.insert("", tk.END, values=r)

    tk.Button(search_frame, text="Search", bg=BLUE, fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=15,
              command=lambda: load(entry.get())).grid(row=0, column=2, padx=8)

    tk.Button(search_frame, text="Reset", bg=RED, fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=15,
              command=lambda: load()).grid(row=0, column=3, padx=8)

    load()


def classpulse_analysis():
    avg, sessions, low, distracted, best = get_analysis_stats()

    win = tk.Toplevel(root)
    win.title("ClassPulse Analysis")
    win.geometry("900x500")
    win.configure(bg=BG)

    tk.Label(win, text="ClassPulse Analysis", bg=BG, fg="#38bdf8",
             font=("Segoe UI", 30, "bold")).pack(pady=(35, 8))

    tk.Label(win, text="AI-powered classroom engagement summary", bg=BG, fg=MUTED,
             font=("Segoe UI", 13)).pack(pady=(0, 25))

    frame = tk.Frame(win, bg=BG)
    frame.pack()

    cards = [
        ("📊 Average Attention", f"{avg}%", TEAL),
        ("🧠 Total Sessions", sessions, BLUE),
        ("⚠ Low Engagement", low, RED),
        ("📉 Most Distracted", distracted, "#7f1d1d"),
        ("🏆 Best Student", best, GREEN),
    ]

    for i, (title, value, color) in enumerate(cards):
        tk.Label(frame, text=f"{title}\n{value}", bg=color, fg="white",
                 font=("Segoe UI", 14, "bold"), width=24, height=4)\
            .grid(row=i // 2, column=i % 2, padx=15, pady=15)


def generate_parent_alerts():
    win = tk.Toplevel(root)
    win.title("Parent Alert Messages")
    win.geometry("900x600")
    win.configure(bg=DARK)

    tk.Label(win, text="Parent Alert Messages", bg=DARK, fg="#38bdf8",
             font=("Segoe UI", 26, "bold")).pack(pady=20)

    box = tk.Text(win, bg=BG, fg="white", font=("Segoe UI", 11), wrap="word")
    box.pack(fill="both", expand=True, padx=20, pady=20)

    rows = db_fetch("""
        SELECT name, date, phone_usage, attention_score
        FROM engagement
        WHERE attention_score < 50
        ORDER BY id DESC
    """)

    if not rows:
        box.insert("end", "No low engagement records found.")
    else:
        for name, date, phone, score in rows:
            box.insert("end", f"""
Dear Parent,

This is to inform you that {name} showed low classroom engagement on {date}.
The recorded attention score was {score:.2f}% and phone usage was {phone:.2f}% during the monitored session.

Please encourage the student to stay more attentive during class.

Regards,
ClassPulse AI Monitoring System

------------------------------------------------------------

""")
    box.config(state="disabled")


def input_name():
    win = tk.Toplevel(root)
    win.title("Enter Student Name")
    win.geometry("400x180")
    win.configure(bg=BG)

    value = tk.StringVar()

    tk.Label(win, text="Enter student name:", bg=BG, fg=TEXT,
             font=("Segoe UI", 13, "bold")).pack(pady=20)

    entry = tk.Entry(win, font=("Segoe UI", 12), width=30)
    entry.pack()

    tk.Button(win, text="Submit", bg=BLUE, fg="white", bd=0,
              font=("Segoe UI", 11, "bold"),
              command=lambda: (value.set(entry.get()), win.destroy())).pack(pady=15)

    win.wait_window()
    return value.get()


def view_personal_report(role):
    name = input_name()
    if not name:
        return

    table_window(
        f"{role} Report",
        ("Name", "Date", "Duration", "Face Presence", "Phone Usage", "Attention Score", "Status"),
        """
        SELECT name, date, session_duration, face_presence, phone_usage, attention_score, status
        FROM engagement
        WHERE name LIKE '%{}%'
        """.format(name),
        "1050x500"
    )


def clear():
    for w in root.winfo_children():
        w.destroy()


def button(parent, text, cmd, color):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        font=("Segoe UI", 13, "bold"),
        width=42,
        height=2,
        bd=0,
        cursor="hand2"
    )


def top_button(text, cmd, x, color):
    tk.Button(root, text=text, command=cmd, bg=color, fg="white",
              font=("Segoe UI", 11, "bold"), width=18, height=1,
              bd=0, cursor="hand2").place(x=x, y=25)


def role_selection_screen():
    clear()
    root.geometry("900x700")
    root.configure(bg=BG)

    tk.Label(root, text="ClassPulse AI", bg=BG, fg="#38bdf8",
             font=("Segoe UI", 38, "bold")).pack(pady=(70, 10))

    tk.Label(root, text="Select Your Role", bg=BG, fg=MUTED,
             font=("Segoe UI", 16)).pack(pady=(0, 40))

    card = tk.Frame(root, bg=CARD, padx=55, pady=45)
    card.pack()

    button(card, "👨‍🏫  Teacher Login", teacher_dashboard, BLUE).pack(pady=12)
    button(card, "👨‍👩‍👧  Parent Login", parent_dashboard, GREEN).pack(pady=12)
    button(card, "👨‍🎓  Student Login", student_dashboard, PURPLE).pack(pady=12)
    button(card, "⏻  Exit", root.quit, RED).pack(pady=12)


def teacher_dashboard():
    clear()
    root.geometry("1200x900")
    root.configure(bg=BG)

    top_button("← Back", role_selection_screen, 30, "#334155")
    # ================= DROPDOWN MENU =================

    menu_button = tk.Menubutton(
        root,
        text="☰ Menu",
        bg="#1e293b",
        fg="white",
        activebackground="#334155",
        activeforeground="white",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2"
    )

    menu_button.place(x=1030, y=25)

    menu = tk.Menu(
        menu_button,
        tearoff=0,
        bg="#111827",
        fg="white",
        activebackground="#2563eb",
        activeforeground="white",
        font=("Segoe UI", 11)
    )

    menu.add_command(
        label="📁 Export Attendance",
        command=export_attendance
    )

    menu.add_command(
        label="🚨 Parent Alerts",
        command=generate_parent_alerts
    )

    menu.add_separator()

    menu.add_command(
        label="⏻ Exit",
        command=root.quit
    )

    menu_button.config(menu=menu)

    tk.Label(root, text="Teacher Dashboard", bg=BG, fg="#38bdf8",
             font=("Segoe UI", 34, "bold")).pack(pady=(60, 5))

    tk.Label(root, text="AI Powered Classroom Monitoring", bg=BG, fg=MUTED,
             font=("Segoe UI", 13)).pack(pady=(0, 25))

    students, attendance = get_stats()

    stats = tk.Frame(root, bg=BG)
    stats.pack(pady=10)

    tk.Label(stats, text=f"👥 Total Students\n{students}", bg=CARD, fg="white",
             font=("Segoe UI", 15, "bold"), width=22, height=4).grid(row=0, column=0, padx=18)

    tk.Label(stats, text=f"☑ Attendance Records\n{attendance}", bg=CARD, fg="white",
             font=("Segoe UI", 15, "bold"), width=26, height=4).grid(row=0, column=1, padx=18)

    card = tk.Frame(root, bg=CARD, padx=50, pady=35)
    card.pack(pady=35)

    button(card, "👤➕  Register Student", register_student, BLUE).pack(pady=9)
    button(card, "🧠  Start Measuring ClassPulse", lambda: run_script("classroom_monitor.py"), GREEN).pack(pady=9)
    button(card, "📋  View Attendance", view_attendance, PURPLE).pack(pady=9)
    button(card, "👥  View Students", view_students, ORANGE).pack(pady=9)
    button(card, "📈  View Engagement Reports", view_engagement, TEAL).pack(pady=9)
    button(card, "📊  ClassPulse Analysis", classpulse_analysis, "#1d4ed8").pack(pady=9)
    tk.Label(
    root,
    text="ClassPulse AI • Smart Classroom Monitoring System • v1.0",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(side="bottom", pady=18)


def parent_dashboard():
    clear()
    root.geometry("900x650")
    root.configure(bg=BG)

    top_button("← Back", role_selection_screen, 30, "#334155")

    tk.Label(root, text="Parent Dashboard", bg=BG, fg="#38bdf8",
             font=("Segoe UI", 34, "bold")).pack(pady=(80, 10))

    tk.Label(root, text="View your child's attendance and engagement report", bg=BG, fg=MUTED,
             font=("Segoe UI", 13)).pack(pady=(0, 40))

    card = tk.Frame(root, bg=CARD, padx=55, pady=45)
    card.pack()

    button(card, "📈  View Child Engagement Report", lambda: view_personal_report("Parent"), GREEN).pack(pady=12)
    button(card, "📋  View Attendance Records", view_attendance, PURPLE).pack(pady=12)


def student_dashboard():
    clear()
    root.geometry("900x700")
    root.configure(bg=BG)

    top_button("← Back", role_selection_screen, 30, "#334155")

    tk.Label(root, text="Student Dashboard", bg=BG, fg="#38bdf8",
             font=("Segoe UI", 34, "bold")).pack(pady=(80, 10))

    tk.Label(root, text="Register yourself and track your engagement", bg=BG, fg=MUTED,
             font=("Segoe UI", 13)).pack(pady=(0, 40))

    card = tk.Frame(root, bg=CARD, padx=55, pady=45)
    card.pack()

    button(card, "👤➕  Register Myself", register_student, BLUE).pack(pady=12)
    button(card, "📈  View My Engagement Report", lambda: view_personal_report("Student"), PURPLE).pack(pady=12)
    button(card, "📋  View Attendance Records", view_attendance, CYAN).pack(pady=12)


root = tk.Tk()
root.title("ClassPulse AI")
role_selection_screen()
root.mainloop()