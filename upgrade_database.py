import sqlite3

conn = sqlite3.connect("classpulse.db")
cursor = conn.cursor()

# Add roll_no column if not exists
try:
    cursor.execute("ALTER TABLE attendance ADD COLUMN roll_no TEXT")
    print("roll_no column added")
except sqlite3.OperationalError:
    print("roll_no column already exists")

# Add class_name column if not exists
try:
    cursor.execute("ALTER TABLE attendance ADD COLUMN class_name TEXT")
    print("class_name column added")
except sqlite3.OperationalError:
    print("class_name column already exists")

conn.commit()
conn.close()

print("Database upgraded successfully!")