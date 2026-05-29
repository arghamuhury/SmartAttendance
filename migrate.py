import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add latitude
    try:
        cursor.execute("ALTER TABLE attendance_sessions ADD COLUMN latitude FLOAT")
        print("Successfully added latitude column.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")
        
    # Add longitude
    try:
        cursor.execute("ALTER TABLE attendance_sessions ADD COLUMN longitude FLOAT")
        print("Successfully added longitude column.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")
        
    conn.commit()
    conn.close()
    print("Database migration complete!")
except Exception as e:
    print(f"Error connecting to database: {e}")
