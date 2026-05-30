from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openpyxl import Workbook
from io import BytesIO
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "../classpulse.db"


class StudentCreate(BaseModel):
    name: str
    roll_no: str
    class_name: str
    phone: str


def fetch_one(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] is not None else 0


def fetch_all(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


@app.get("/")
def home():
    return {"message": "ClassPulse AI Backend Running"}


@app.get("/stats")
def get_stats():
    return {
        "totalStudents": fetch_one("SELECT COUNT(*) FROM students"),
        "attendanceRecords": fetch_one("SELECT COUNT(*) FROM attendance"),
        "avgAttention": round(fetch_one("SELECT AVG(attention_score) FROM engagement"), 2),
        "lowEngagement": fetch_one("SELECT COUNT(*) FROM engagement WHERE attention_score < 50"),
    }


@app.get("/students")
def get_students():
    return fetch_all("SELECT id, name, roll_no, class_name, phone FROM students")


@app.get("/attendance")
def get_attendance():
    return fetch_all("""
        SELECT id, name, roll_no, class_name, date, time
        FROM attendance
        ORDER BY id DESC
    """)


@app.get("/engagement")
def get_engagement():
    return fetch_all("""
        SELECT id, name, date, session_duration, face_presence, phone_usage, attention_score, status
        FROM engagement
        ORDER BY id DESC
    """)


@app.post("/register-student")
def register_student(student: StudentCreate):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE roll_no=?",
            (student.roll_no,)
        )

        existing = cursor.fetchone()

        if existing:
            conn.close()
            raise HTTPException(status_code=400, detail="Roll number already exists")

        cursor.execute("""
            INSERT INTO students (name, roll_no, class_name, phone)
            VALUES (?, ?, ?, ?)
        """, (
            student.name,
            student.roll_no,
            student.class_name,
            student.phone
        ))

        conn.commit()
        conn.close()

        return {"message": "Student registered successfully"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/parent-alerts")
def get_parent_alerts():
    records = fetch_all("""
        SELECT name, date, phone_usage, attention_score, status
        FROM engagement
        WHERE attention_score < 50
        ORDER BY id DESC
    """)

    alerts = []

    for record in records:
        alerts.append({
            "name": record["name"],
            "date": record["date"],
            "phoneUsage": record["phone_usage"],
            "attentionScore": record["attention_score"],
            "message": f"Dear Parent, {record['name']} showed low classroom engagement on {record['date']}. The recorded attention score was {record['attention_score']:.2f}% and phone usage was {record['phone_usage']:.2f}% during the monitored session."
        })

    return alerts


@app.get("/export-attendance")
def export_attendance():
    rows = fetch_all("""
        SELECT id, name, roll_no, class_name, date, time
        FROM attendance
        ORDER BY id DESC
    """)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Attendance Report"

    sheet.append(["ID", "Name", "Roll No", "Class", "Date", "Time"])

    for row in rows:
        sheet.append([
            row["id"],
            row["name"],
            row["roll_no"],
            row["class_name"],
            row["date"],
            row["time"],
        ])

    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=attendance_report.xlsx"}
    )