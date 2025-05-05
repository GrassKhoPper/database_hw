import os
import psycopg
import hashlib

from flask import g

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

def authenticate(username:int, password:str):
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT *
			FROM accounts 
			WHERE uuid = (%s);
		""", (username,))
		data = cursor.fetchone()
		if data and hashlib.md5(password.encode()).hexdigest() == data['phash']:
			return {'id': data['id'], 'uuid': data['uuid']}
		return None
	except psycopg.Error as e:
		raise ValueError(f'sql error in auth:{e}') from e

def get_user_balance(user_id:int):
	try:
		cursor = get_db().cursor()
		cursor.execute("""
			SELECT balance
			FROM accounts 
			WHERE id = (%s);
		""", (user_id,))
		data = cursor.fetchone()
	except psycopg.Error as e:
		raise ValueError(f'sql error:{e}') from e
	if data: 
		return data['balance']
	raise ValueError('No user with this id')

def add_account(uuid:str, password:str):
	phash = hashlib.md5(password.encode()).hexdigest()
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO accounts (uuid, phash, balance)
			VALUES (%s, %s, 100000);
		""", (uuid, phash,))
		conn.commit()
		return {
			'id' : cursor.lastrowid,
			'uuid' : uuid,
			'balance' : 100000
		}
	except psycopg.Error as e:
		conn.rollback()
		raise ValueError(f'sql error:{e}') from e

def delete_account(user_id:int):
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("""
			DELETE FROM accounts
			WHERE id = %s;
		""", (user_id,))
		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		raise ValueError(f'sql error:{e}') from e

def transfer(id_from:int, uuid_to:str, amount:int):
	conn = get_db()
	cursor = conn.cursor()
	try:
		cursor.execute('BEGIN TRANSACTION')
		cursor.execute(
			'SELECT id FROM accounts WHERE uuid = %s;',
			(uuid_to,)
		)
		id_to = cursor.fetchone()
		if not id_to:
			raise ValueError(f'No recver uuid={uuid_to} in database')
		id_to = id_to['id']

		cursor.execute(
			'SELECT balance FROM accounts WHERE id = %s;',
			(id_from,)
		)
		sender_balance = cursor.fetchone()
		if not sender_balance or sender_balance['balance'] < amount:
			raise ValueError('Not enough money :(')

		cursor.execute(
			'UPDATE accounts SET balance = balance - %s WHERE id = %s;', 
			(amount, id_from,)
		)
		cursor.execute(
			'UPDATE accounts SET balance = balance + %s WHERE id = %s;',
			(amount, id_to,)
		)

		cursor.execute(
			'INSERT INTO transactions (user_id, amount) VALUES (%s, %s), (%s, %s);', 
			(id_from, -amount, id_to, amount)
		)

		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		raise e from e
	except ValueError as e:
		conn.rollback()
		raise e from e
