import sqlite3


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            status TEXT NOT NULL    
        )   
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deptCode TEXT NOT NULL,
            deptName TEXT NOT NULL,
            location TEXT NOT NULL         
        )    
    """)
    conn.commit()
    conn.close()
