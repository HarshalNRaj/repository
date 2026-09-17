import os
import sqlite3
from werkzeug.security import generate_password_hash

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
print("Target DB path:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ensure table schema is checked
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

cursor.execute('''
    INSERT OR REPLACE INTO users (name, email, password_hash, phone, role, is_verified)
    VALUES (?, ?, ?, ?, ?, 1)
''', ('System Admin', 'admin@resqlink.com', generate_password_hash('Admin@123'), '9999999999', 'admin'))

conn.commit()
print("SUCCESS: Admin user seeded into database.db")
