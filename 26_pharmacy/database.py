import sqlite3


def get_db():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      
            medicineName TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            contactNumber TEXT NOT NULL,
            address TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customerName TEXT NOT NULL,
            medicineName TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            totalPrice REAL NOT NULL,
            saleDate TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
