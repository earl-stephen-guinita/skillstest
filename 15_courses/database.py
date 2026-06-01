import sqlite3


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            courseCode TEXT NOT NULL,
            courseName TEXT NOT NULL,
            units INTEGER NOT NULL,
            department TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
