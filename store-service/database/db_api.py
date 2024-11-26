import sqlite3
import os
from flask import g

DB_PATH = os.environ.get('DB_PATH', '/var/store-db/store.sql3.db')

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(f'Can not create connection to database: {e}')
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

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(DB_PATH)
		g.db.isolation_level = None
		g.db.row_factory = sqlite3.Row
	return g.db

def get_games_list()->list[dict]:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute('SELECT * FROM games;')
		games_data = cursor.fetchall()
		games = [dict(game_data) for game_data in games_data]
		return games
	except sqlite3.Error as e:
		print(f'sql execution error {e}')
		return None

def get_game_by_id(game_id:int)->dict:
	db = get_db()
	cursor = db.cursor()

	try:
		cursor.execute(
			"SELECT * FROM games WHERE id = ?", (game_id,)
		)
		game_data = dict(cursor.fetchone())
		if game_data:
			return game_data
		else:
			return None
	except sqlite3.Error as e:
		print(f'execute game query with id={game_id}:{e}')
		return None

