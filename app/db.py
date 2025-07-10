import sqlite3
import os

def init_db():
    BANCO = os.getenv('BANCO', 'app/data.db')
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT
        )
    ''')
    conn.commit()
    conn.close()
