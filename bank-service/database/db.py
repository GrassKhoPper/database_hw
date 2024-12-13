import os
import sqlite3
import hashlib

from flask import g

DB_PATH = os.environ.get('DB_PATH', '/var/bank-db/bank.sql3.db')

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(DB_PATH)
		g.db.row_factory = sqlite3.Row
	return g.db

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
	init_files = ['database/bank-schema.sql', 'database/bank-init.sql']
	conn = sqlite3.connect(DB_PATH)
	if conn:
		_ = [execute_sql_file(conn, x) for x in init_files]
		conn.close()
	else:
		raise ValueError('Can not create connection to database')

def authenticate(username:int, password:str):
	cursor = get_db().cursor()
	try:
		cursor.execute("""
			SELECT *
			FROM accounts 
			WHERE uuid = (?);
		""", (username,))
		data = cursor.fetchone()
		if data and hashlib.md5(password.encode()).hexdigest() == data['phash']:
			return {'id': data['id'], 'uuid': data['uuid']}
		return None
	except sqlite3.Error as e:
		raise ValueError(f'sqlite error in auth:{e}') from e

def get_user_balance(user_id:int):
	try:
		cursor = get_db().cursor()
		cursor.execute("""
			SELECT balance
			FROM accounts 
			WHERE id = (?);
		""", (user_id,))
		data = cursor.fetchone()
	except sqlite3.Error as e:
		raise ValueError(f'sqlite3 error:{e}') from e
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
			VALUES (?, ?, 100000);
		""", (uuid, phash,))
		conn.commit()
		return {
			'id' : cursor.lastrowid,
			'uuid' : uuid,
			'balance' : 100000
		}
	except sqlite3.Error as e:
		conn.rollback()
		raise ValueError(f'sqlite3 error:{e}') from e

def delete_account(user_id:int):
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("""
			DELETE FROM accounts
			WHERE id = (?);
		""", (user_id,))
		conn.commit()
	except sqlite3.Error as e:
		conn.rollback()
		raise ValueError(f'sqlite3 error:{e}') from e

def transfer(id_from:int, uuid_to:str, amount:int):
	conn = get_db()
	cursor = conn.cursor()
	try:
		cursor.execute('BEGIN TRANSACTION')
		cursor.execute(
			'SELECT id FROM accounts WHERE uuid = (?);',
			(uuid_to,)
		)
		id_to = cursor.fetchone()
		if not id_to:
			raise ValueError(f'No recver uuid={uuid_to} in database')
		id_to = id_to['id']

		cursor.execute(
			'SELECT balance FROM accounts WHERE id = (?);',
			(id_from,)
		)
		sender_balance = cursor.fetchone()
		if not sender_balance or sender_balance['balance'] < amount:
			raise ValueError('Not enough money :(')

		cursor.execute(
			'UPDATE accounts SET balance = balance - (?) WHERE id = (?);', 
			(amount, id_from,)
		)
		cursor.execute(
			'UPDATE accounts SET balance = balance + (?) WHERE id = (?);',
			(amount, id_to,)
		)

		cursor.execute(
			'INSERT INTO transactions (user_id, amount) VALUES (?, ?), (?, ?);', 
			(id_from, -amount, id_to, amount)
		)

		conn.commit()
	except sqlite3.Error as e:
		conn.rollback()
		raise e from e
	except ValueError as e:
		conn.rollback()
		raise e from e
