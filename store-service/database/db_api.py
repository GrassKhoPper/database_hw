import sqlite3
import os
from flask import g

from utility.User import User
from utility.Game import Game

DB_PATH = os.environ.get('DB_PATH', '/var/store-db/store.sql3.db')

# def init_database_from_csv(db_path:str, csv_folder:str):
# 	tables = {
# 		'games' : 'games.csv',
# 		'studios' : 'studios.csv',
# 		'tags' : 'tags.csv',
# 		'game_tags' : 'game_tags.csv',
# 		'games_pictures' : 'games_pictures.csv',
# 		'profiles_pictures': 'profiles_pictures.csv'
# 	}
# 	try:
# 		pass
# 	except:
# 		pass

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(f'Can not create connection to database: {e}')
		raise e
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
		user_data = cursor.fetchone()

		if not user_data:
			raise ValueError('Unknown username')

		user_data = dict(user_data)
		if user_data['password_hash'] == user.phash:
			return user_data['id']
		else:
			raise ValueError('Wrong password')

	except sqlite3.Error as e:
		raise ValueError(str(e))

def add_user(user:User):
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			INSERT INTO users (name, password_hash)
			VALUES (?, ?)
		""", (user.name, user.phash))
		print(f'user add query was called')
		db.commit()

	except sqlite3.Error as e:
		print(f'sqlite3 error:{e}')
		raise ValueError(str(e))

def get_profile_picture(user_id:int)->str:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			SELECT pp.name, pp.img_fmt
			FROM users u
			JOIN profiles_pictures pp ON u.id = pp.user_id
			WHERE u.id = ?;
		""", (user_id,))
		user_pic = cursor.fetchone()
		if not user_pic:
			user_pic = 'default.jpg'
		else:
			user_pic = dict(user_pic)
			user_pic = user_pic['name'] if 'name' in user_pic else 'default.jpg'
		return user_pic
	except sqlite3.Error as e:
		print(f'sql error:{e}')
		raise ValueError(str(e))

def get_games_for_library(uid:int)->list[Game]:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			SELECT g.*, s.name AS studio_name,
				GROUP_CONCAT(DISTINCT t.name) AS tags,
				GROUP_CONCAT(DISTINCT p.name || ':' || p.img_type || ':' || p.img_fmt) AS pictures,
				(SELECT p.name FROM games_pictures p WHERE p.game_id = g.id AND p.img_type = 'cover') AS cover_image
			FROM games g
			JOIN studios s ON g.studio_id = s.id
			LEFT JOIN game_tags gt ON g.id = gt.game_id
			LEFT JOIN tags t ON gt.tag_id = t.id
			LEFT JOIN games_pictures p ON g.id = p.game_id
			JOIN purchases pur ON g.id = pur.game_id 
			WHERE pur.owner_id = ?
			GROUP BY g.id;
		""", (uid,))
		games_data = cursor.fetchall()
		games_data = [Game(dict(game)) for game in games_data] if games_data else []
		print(games_data)
		return games_data

	except sqlite3.Error as e:
		raise ValueError(str(e))

