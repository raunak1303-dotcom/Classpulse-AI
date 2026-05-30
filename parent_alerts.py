import sqlite3

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

cursor.execute("""
SELECT name, date, phone_usage, attention_score, status
FROM engagement
WHERE attention_score < 50
ORDER BY id DESC
""")

records = cursor.fetchall()

print("\n===== PARENT ALERT MESSAGES =====\n")

if not records:
    print("No low engagement records found.")
else:
    for name, date, phone_usage, attention_score, status in records:
        message = f"""
Dear Parent,

This is to inform you that {name} showed low classroom engagement on {date}.
The recorded attention score was {attention_score:.2f}% and phone usage was {phone_usage:.2f}% during the monitored session.

Please encourage the student to stay more attentive during class.

Regards,
ClassPulse AI Monitoring System
"""
        print(message)
        print("-" * 60)

conn.close()