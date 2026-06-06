import sqlite3


def get_db():
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            course TEXT NOT NULL,
            yearLevel INTEGER NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            subject TEXT NOT NULL,
            contactNumber TEXT NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subjectCode TEXT NOT NULL,
            subjectName TEXT NOT NULL,
            units INTEGER NOT NULL,
            department TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
