import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".rewind.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT
        )
        """)
        self.conn.commit()

    def add_event(self, category, title, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
        INSERT INTO events (timestamp, category, title, details)
        VALUES (?, ?, ?, ?)
        """, (timestamp, category, title, details))

        self.conn.commit()

    def get_all_events(self):
        self.cursor.execute("""
        SELECT id, timestamp, category, title, details
        FROM events
        ORDER BY timestamp DESC
        """)

        return self.cursor.fetchall()

    def get_events_by_date(self, date):
        self.cursor.execute("""
        SELECT timestamp, category, title, details
        FROM events
        WHERE DATE(timestamp) = ?
        ORDER BY timestamp
        """, (date,))

        return self.cursor.fetchall()

    def search_events(self, keyword):
        self.cursor.execute("""
        SELECT timestamp, category, title, details
        FROM events
        WHERE title LIKE ? OR details LIKE ?
        ORDER BY timestamp DESC
        """, (f"%{keyword}%", f"%{keyword}%"))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()