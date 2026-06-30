import sqlite3


def get_db():
    conn = sqlite3.connect("restaurant.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            itemName TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL         
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customerName TEXT NOT NULL,
            itemName TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            totalPrice REAL NOT NULL,
            orderDate TEXT NOT NULL         
        )
    """)
    conn.commit()
    conn.close()
