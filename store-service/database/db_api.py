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
		raise e
	return conn

def execute_sql_file(conn, sql_file):
	try:
		with open(sql_file, 'r', encoding='UTF-8') as file:
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
		_ = [execute_sql_file(conn, x) for x in init_files]
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
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT id 
			FROM games;
		""")
		game_ids = cursor.fetchall()
		# TODO: not optimal to get elements one by one 
		# ( but mb it is better cause we can load games from id_beg to id_end)
		games = [get_game_info(game_id['id']) for game_id in game_ids]
		return games
	except sqlite3.Error as e:
		print(f'sql execution error {e}')
		return None

def get_game_info(game_id:int)->dict:
	tags = get_tags_by_game_id(game_id)
	pictures = get_pictures_by_game_id(game_id)
	
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT g.*, s.name AS studio_name
			FROM games g
			JOIN studios s ON s.id = g.studio_id
			WHERE g.id = (?);
		""", (game_id,))
		data = dict(cursor.fetchone())
		data['tags'] = tags
		data['pictures'] = pictures		
		return data
	except sqlite3.Error as e:
		print(f'execute game query with id={game_id}:{e}')
		return None

def check_user(user:User)->int:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute(
			'SELECT * FROM users WHERE name = (?);', (user.name,)
		)
		user_data = cursor.fetchone()

		if not user_data:
			raise ValueError('Unknown username')

		user_data = dict(user_data)
		if user_data['password_hash'] == user.phash:
			return user_data['id'], user_data['balance']
		raise ValueError('Wrong password')

	except sqlite3.Error as e:
		raise ValueError(str(e)) from e

def add_user(user:User):
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			INSERT INTO users (name, password_hash, balance)
			VALUES (?, ?, ?)
		""", (user.name, user.phash, 0))
		print('user add query was called')
		db.commit()

	except sqlite3.Error as e:
		print(f'sqlite3 error:{e}')
		raise ValueError(str(e)) from e

def get_profile_picture(user_id:int)->str:
	cursor = get_db().cursor()
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
		raise ValueError(str(e)) from e

def get_user_games_in_library(user_id:int)->list[dict]:
	try:
		user_game_ids = get_user_games(user_id)
		games = [get_game_info(game_id) for game_id in user_game_ids]
		return games
	except Exception as e:
		raise ValueError('strange get games for library error') from e

def get_user_games(user_id:int)->list[int]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT game_id 
			FROM purchases 
			WHERE owner_id = (?) AND ts IS NOT NULL;
		""", (user_id,))

		return [x['game_id'] for x in cursor.fetchall()]
	except sqlite3.Error as e:
		print(f'sqlite error:{e}')
		raise ValueError(f'{e}') from e

def get_tags_by_game_id(game_id:int)->list[str]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT t.name
			FROM game_tags gt
			JOIN tags t ON gt.tag_id = t.id
			WHERE gt.game_id = ?;
		""", (game_id,))
		data = cursor.fetchall()
		tags = [tag['name'] for tag in data]
		return tags
	except Exception as e:
		raise ValueError('error on getting game tags') from e

def get_pictures_by_game_id(game_id:int)->list[str]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT name, img_type, img_fmt
			FROM games_pictures 
			WHERE game_id = ?;
		""", (game_id,))
		data = cursor.fetchall()
		return data
	except Exception as e:
		raise ValueError('suddenly causing error') from e
	
def buy_cart(user_id:int, total:int, games_ids:list[int]):
	conn = get_db()
	cursor = conn.cursor()
	print(f'games_ids:{games_ids}')
	try:
		placeholders = ', '.join(['?'] * len(games_ids))
		# change purchases
		cursor.execute(f"""
			UPDATE purchases 
			SET ts = STRFTIME('%s', 'now')
			WHERE owner_id = (?) AND game_id IN ({placeholders}) AND ts IS NULL;
		""", [user_id] + games_ids)
		# change balance
		cursor.execute("""
			UPDATE users
			SET balance = balance - (?)
			WHERE id = (?);
		""", (total, user_id,))
		conn.commit()
	except sqlite3.Error as e:
		conn.rollback()
		print('something went wrong')
		raise e from e

def remove_from_cart(user_id:int, game_id:int):
	conn   = get_db()
	cursor = conn.cursor()
	try:
		cursor.execute("""
			DELETE FROM purchases 
			WHERE owner_id = (?) AND game_id = (?) AND ts IS NULL;
		""", (user_id, game_id,))
		conn.commit()
	except sqlite3.Error as e:
		conn.rollback()
		raise ValueError(e) from e

def get_user_cart_games(user_id:int)->list[dict]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT game_id 
			FROM purchases 
			WHERE owner_id == (?) and ts IS NULL;
		""", (user_id,))
		data = cursor.fetchall()
		return data
	except sqlite3.error as e:
		raise ValueError(f'sqlite3 error: {e}') from e
