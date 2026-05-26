import sqlite3

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM attendance")

records = cursor.fetchall()

print("\n===== CLASSPULSE AI ATTENDANCE =====\n")

for record in records:
    print(record)

conn.close()