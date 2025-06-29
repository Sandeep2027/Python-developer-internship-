import sqlite3

def get_db_connection():
    conn = sqlite3.connect("events.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        ''')