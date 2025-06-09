import os
import psycopg
import bcrypt

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
		except psycopg.OperationalError as e:
			raise ValueError(f'Failed to connect to database: {e}')	
	return g.db

def authenticate(username:int, password:str):
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT *
			FROM bank.accounts 
			WHERE uuid = (%s);
		""", (username,))
		data = cursor.fetchone()
		if data and bcrypt.checkpw(password.encode('utf-8'), data['phash'].encode('utf-8')):
			return {'id': data['id'], 'uuid': data['uuid']}
		return None
	except psycopg.Error as e:
		raise ValueError(f'sql error in auth:{e}') from e

def get_user_balance(user_id:int):
	try:
		cursor = get_db().cursor()
		cursor.execute("""
			SELECT balance
			FROM bank.accounts 
			WHERE id = (%s);
		""", (user_id,))
		data = cursor.fetchone()
	except psycopg.Error as e:
		raise ValueError(f'sql error:{e}') from e
	if data: 
		return data['balance']
	raise ValueError('No user with this id')

def add_account(uuid:str, password:str):
	phash = bcrypt.hashpw(
		password.encode('utf-8'),
		bcrypt.gensalt(rounds = 12)
	).hexdigest()
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO bank.accounts (uuid, phash, balance)
			VALUES (%s, %s, 100000)
			RETURNING id, uuid, balance;
		""", (uuid, phash,))
		r = cursor.fetchone()
		conn.commit()
		return {
			'id' :      r['id'],
			'uuid' :    r['uuid'],
			'balance' : r['balance']
		}
	except psycopg.Error as e:
		conn.rollback()
		raise ValueError(f'sql error:{e}') from e

def delete_account(user_id:int):
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("""
			DELETE FROM bank.accounts
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
			'SELECT id, uuid FROM bank.accounts WHERE uuid = %s;',
			(uuid_to,)
		)
		id_to = cursor.fetchone()
		if not id_to:
			raise ValueError(f'No recver uuid={uuid_to} in database')
		id_to   = id_to['id']
		uuid_to = id_to['uuid']

		cursor.execute(
			'SELECT id, uuid, balance FROM bank.accounts WHERE id = %s;',
			(id_from,)
		)

		from_data = cursor.fetchone()
		if not from_data:
			raise ValueError(f'No sender with id={id_from} in database')
		uuid_from = from_data['uuid']

		if id_from == id_to:
			raise ValueError('Why you need to send money for yourself???')

		if from_data['balance'] < amount:
			raise ValueError('Not enough money :(')

		cursor.execute(
			'INSERT INTO bank.transactions (account_id, amount, account_uuid_snapshot) VALUES (%s, %s, %s);',
			(id_from, -amount, uuid_from)
		)

		cursor.execute(
			'INSERT INTO bank.transactions (account_id, amount, account_uuid_snapshot) VALUES (%s, %s, %s);',
			(id_to, amount, uuid_to)
		)

		conn.commit()
	except psycopg.Error as e:
		conn.rollback()
		raise e from e
	except ValueError as e:
		conn.rollback()
		raise e from e
