import sqlite3

db_file = "studybuddy.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE note ADD COLUMN folder VARCHAR DEFAULT 'General'")
    print("Column 'folder' added successfully.")
except sqlite3.OperationalError as e:
    print(f"Column might already exist: {e}")

conn.commit()
conn.close()
