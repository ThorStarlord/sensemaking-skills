import sqlite3
from pathlib import Path

def get_db():
    conn = sqlite3.connect(Path("notes.db"))
    conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)")
    return conn
