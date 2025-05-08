import psycopg
import os
import csv
import base64
import io

from PIL import Image
from flask import g

from store.utility.User import User

INIT_CSV_PATH = os.environ.get('INIT_CSV_PATH', '/tmp/init-csvs')
STATIC_PATH = os.environ.get('STATIC_PATH', '/store/store/static')

def init_pics_from_csv(csv_file:str, table_name:str, save_to:str):
	try:
		with open(csv_file, 'r', encoding='UTF-8') as file:
			reader = csv.reader(file)
			headers = next(reader)[:-1]

			for row in reader:
				if save_to == 'profiles':
					img, data, path = base64.b64decode(row[-1]), row[:-1], f'{row[0]}p.png'
					img = Image.open(io.BytesIO(img))
					img.save(f'{STATIC_PATH}/images/{save_to}/{path}')
				else :
					img, data = base64.b64decode(row[-1]), row[:-1]
					img = Image.open(io.BytesIO(img))
					game_id, path = data[2], f'{row[0]}g.{row[-2]}'
					os.makedirs(f'{STATIC_PATH}/images/{save_to}/{game_id}', exist_ok=True)
					img.save(f'{STATIC_PATH}/images/{save_to}/{game_id}/{path}')
	except Exception as e:
		print(f'init pictures error:{e}')
		raise ValueError(str(e)) from e

def init_database():
	init_pics_csvs = [{
		'file': f'{INIT_CSV_PATH}/init-profile-pictures.csv', 
		'table':'profiles_pictures',
		'save_to' : 'profiles'
	}, {
		'file': f'{INIT_CSV_PATH}/init-games-pictures.csv', 
		'table':'games_pictures',
		'save_to' : 'games'
	}]
	try:
		_ = [init_pics_from_csv(
			csv_file=init_pics['file'], 
			table_name=init_pics['table'], 
			save_to=init_pics['save_to']
		) for init_pics in init_pics_csvs]
	except ValueError as e:
		print(f'I have an error:{e}')

def get_db():
	if 'db' not in g:
		conn_params = {
			'host'    : os.getenv('DB_HOST'),
			'port'    : os.getenv('DB_PORT'),
			'dbname'  : os.getenv('DB_NAME'),
			'user'    : os.getenv('DB_USER'),
			'password': os.getenv('DB_PSWD'),
			'row_factory': psycopg.rows.dict_row
		}
		try:
			g.db = psycopg.connect(**conn_params)
			g.db.autocommit = True
		except psycopg.OperationalError as e:
			raise ValueError(f'Failed to connect to database: {e}')
	return g.db

def get_games_list(last_game_id:int, page_sz:int)->list[dict]:
	cursor = get_db().cursor()
	try:
		queue, params = ("""
			SELECT id 
			FROM store.games
			ORDER BY id 
			LIMIT %s;
		""", (page_sz,)) if last_game_id is None else ("""
			SELECT id
			FROM store.games
			WHERE id > %s
			ORDER BY id
			LIMIT %s;
		""", (last_game_id, page_sz,))
		cursor.execute(queue, params)
		game_ids = cursor.fetchall()

		games = [get_game_info(game_id['id']) for game_id in game_ids]
		return games
	except psycopg.OperationalError as e:
		print(f'sql execution error {e}')
		return None

def get_game_info(game_id:int)->dict:
	tags = get_tags_by_game_id(game_id)
	pictures = get_pictures_by_game_id(game_id)
	
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT g.*, s.name AS studio_name
			FROM store.games g
			JOIN store.studios s ON s.id = g.studio_id
			WHERE g.id = %s;
		""", (game_id,))
		data = cursor.fetchone()
		if data:
			data = dict(data)
			data['tags'] = tags
			data['pictures'] = pictures
		else:
			print(game_id)
		return data
	except psycopg.Error as e:
		print(f'execute game query with id={game_id}:{e}')
		return None

def check_user(user:User)->int:
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute(
			'SELECT * FROM store.users WHERE name = %s;', (user.name,)
		)
		user_data = cursor.fetchone()

		if not user_data:
			raise ValueError('Unknown username')

		user_data = dict(user_data)
		if user_data['password_hash'] == user.phash:
			return user_data['id'], user_data['balance']
		raise ValueError('Wrong password')

	except psycopg.Error as e:
		raise ValueError(str(e)) from e

def add_user(user:User):
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			INSERT INTO store.users (name, password_hash, balance)
			VALUES (%s, %s, %s)
		""", (user.name, user.phash, 0))
		print('user add query was called')
		db.commit()
	except psycopg.Error as e:
		print(f'sql error:{e}')
		db.rollback()
		raise ValueError(str(e)) from e

def get_profile_picture(user_id:int)->str:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT pp.name, pp.img_fmt
			FROM store.users u
			JOIN store.profiles_pictures pp ON u.id = pp.user_id
			WHERE u.id = %s;
		""", (user_id,))
		user_pic = cursor.fetchone()
		if not user_pic:
			user_pic = 'default.jpg'
		else:
			user_pic = dict(user_pic)
			user_pic = user_pic['name'] if 'name' in user_pic else 'default.jpg'
		return user_pic
	except psycopg.Error as e:
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
			FROM store.purchases 
			WHERE owner_id = %s AND ts IS NOT NULL;
		""", (user_id,))

		return [x['game_id'] for x in cursor.fetchall()]
	except psycopg.Error as e:
		print(f'sqlite error:{e}')
		raise ValueError(f'{e}') from e

def get_tags_by_game_id(game_id:int)->list[str]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT t.name
			FROM store.game_tags gt
			JOIN store.tags t ON gt.tag_id = t.id
			WHERE gt.game_id = %s;
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
			FROM store.games_pictures 
			WHERE game_id = %s;
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
		placeholders = ', '.join(['%s'] * len(games_ids))
		# change purchases
		cursor.execute(f"""
			UPDATE store.purchases 
			SET ts = EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::INTEGER
			WHERE owner_id = %s AND game_id IN ({placeholders}) AND ts IS NULL;
		""", [user_id] + games_ids)
		# change balance
		cursor.execute("""
			UPDATE store.users
			SET balance = balance - %s
			WHERE id = %s;
		""", (total, user_id,))
		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		print('something went wrong')
		raise e from e

def remove_from_cart(user_id:int, game_id:int):
	conn   = get_db()
	cursor = conn.cursor()
	try:
		cursor.execute("""
			DELETE FROM store.purchases 
			WHERE owner_id = %s AND game_id = %s AND ts IS NULL;
		""", (user_id, game_id,))
		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		raise ValueError(e) from e

def get_user_cart_games(user_id:int)->list[dict]:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT game_id 
			FROM store.purchases 
			WHERE owner_id = %s and ts IS NULL;
		""", (user_id,))
		data = cursor.fetchall()
		return data
	except psycopg.Error as e:
		raise ValueError(f'sql error: {e}') from e

def add_game_to_cart(user_id:int, game_id:int):
	conn = get_db()
	cursor = conn.cursor()
	try:
		cursor.execute("""
			INSERT INTO store.purchases (owner_id, buyer_id, ts, game_id) 
			VALUES (%s, %s, %s, %s);
		""", (user_id, user_id, None, game_id,))
		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		raise ValueError(f'sql error: {e}') from e

def check_own_game(user_id:int, game_id:int)->bool:
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT id FROM store.purchases 
			WHERE game_id = %s and owner_id = %s;
		""", (game_id, user_id,))
		result = cursor.fetchone()
		if result : 
			return True
		return False
	except psycopg.Error as e:
		raise ValueError(f'sql error: {e}') from e
