import sqlite3


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plateNumber TEXT NOT NULL,
            owner TEXT NOT NULL,
            brand TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
