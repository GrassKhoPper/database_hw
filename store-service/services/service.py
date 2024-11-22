import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', '/store.sql3.db')

def get_all_items():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM t1')
        return cur.fetchall()

def add_item(a, b):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO t1(a, b) VALUES (?, ?)', (a, b))
        conn.commit()
