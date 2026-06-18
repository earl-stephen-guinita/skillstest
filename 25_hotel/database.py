import sqlite3


def get_db():
    conn = sqlite3.connect("hotels.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomNumber TEXT NOT NULL,
            roomType TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            contactNumber TEXT NOT NULL,
            checkIn TEXT NOT NULL,
            checkOut TEXT NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guestName TEXT NOT NULL,
            roomNumber TEXT NOT NULL,
            checkIn TEXT NOT NULL,
            checkOut TEXT NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
