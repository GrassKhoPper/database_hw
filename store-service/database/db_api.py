import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', '/var/store-db/store.sql3.db')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def execute_sql_file(conn, sql_file):
    try:
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        print(f'Execution sql error : {e}')
        conn.rollback()

def init_database():
    db_path = DB_PATH
    init_files = ['database/store-db-schema.sql', 'database/store-init.sql']
    conn = create_connection(db_path)
    if conn:
        [execute_sql_file(conn, x) for x in init_files]
        conn.close()
    else:
        print('Can not create connection to database')

