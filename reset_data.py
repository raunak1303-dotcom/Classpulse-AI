import sqlite3

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM engagement")
cursor.execute("DELETE FROM students")

conn.commit()
conn.close()

print("All old student, attendance, and engagement data cleared.")