import sqlite3

connection = sqlite3.connect("applications.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    status TEXT NOT NULL,
    date_applied TEXT,
    notes TEXT
)
""")

connection.commit()
connection.close()

print("Database and table created successfully.")