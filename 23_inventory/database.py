import sqlite3


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productName TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplierName TEXT NOT NULL,
            contactNumber TEXT NOT NULL,
            address TEXT NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
