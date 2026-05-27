import sqlite3

# Connect database
conn = sqlite3.connect("classpulse.db")

cursor = conn.cursor()

# =========================
# STUDENTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    class_name TEXT NOT NULL,
    phone TEXT
)
""")

# =========================
# ATTENDANCE TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    roll_no TEXT,
    class_name TEXT
)
""")

# =========================
# ENGAGEMENT TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS engagement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    session_duration TEXT,
    face_presence REAL,
    phone_usage REAL,
    attention_score REAL,
    status TEXT
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database tables created successfully!")