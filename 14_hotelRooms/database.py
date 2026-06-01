import sqlite3


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotelRooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomNumber TEXT NOT NULL,
            roomType TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
