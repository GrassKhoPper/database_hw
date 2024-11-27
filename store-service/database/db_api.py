import sqlite3
import os
from flask import g

from utility.User import User

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
	init_files = ['database/store-schema.sql', 'database/store-init.sql']
	conn = create_connection(DB_PATH)
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
		cursor.execute("""
			SELECT g.*, s.name AS studio_name,
      	GROUP_CONCAT(DISTINCT p.name || ':' || p.img_type || ':' || p.img_fmt) AS pictures
			FROM games g
			JOIN studios s ON g.studio_id = s.id
			LEFT JOIN games_pictures p ON g.id = p.game_id
			GROUP BY g.id;
		""")
		games_data = cursor.fetchall()
		games = [dict(game_data) for game_data in games_data]
		print()
		print(games)
		print()
		return games
	except sqlite3.Error as e:
		print(f'sql execution error {e}')
		return None

def get_game_by_id(game_id:int)->dict:
	db = get_db()
	cursor = db.cursor()

	try:
		cursor.execute("""
			SELECT g.*, s.name AS studio_name,
				GROUP_CONCAT(DISTINCT t.name) AS tags,
				GROUP_CONCAT(DISTINCT p.name || ':' || p.img_type || ':' || p.img_fmt) AS pictures
			FROM games g
			JOIN studios s ON g.studio_id = s.id
			LEFT JOIN game_tags gt ON g.id = gt.game_id
			LEFT JOIN tags t ON gt.tag_id = t.id
			LEFT JOIN games_pictures p ON g.id = p.game_id
			WHERE g.id = ?
		""", (game_id,))

		game_data = dict(cursor.fetchone())
		if game_data:
			return game_data
		else:
			return None
	except sqlite3.Error as e:
		print(f'execute game query with id={game_id}:{e}')
		return None

def check_user(user:User)->int:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute(
			'SELECT * FROM users WHERE name = ?', (user.name,)
		)
		user_data = dict(cursor.fetchone())
		if user_data['password_hash'] == user.phash:
			return user_data['id']
		else:
			raise ValueError('wrong password')
	except sqlite3.Error as e:
		raise ValueError(e)

def add_user(user:User)->bool:
	return False

