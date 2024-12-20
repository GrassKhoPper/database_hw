"""
Database module for GameHub Bank application.

"""

import os
import sqlite3
import hashlib

from flask import g

DB_PATH = os.environ.get('DB_PATH', '/var/bank-db/bank.sql3.db')

def get_db():
	"""
    Get database connection from Flask application context.
    
    Returns:
        sqlite3.Connection: Database connection object with Row factory enabled
  """
	if 'db' not in g:
		g.db = sqlite3.connect(DB_PATH)
		g.db.row_factory = sqlite3.Row
	return g.db

def execute_sql_file(conn, sql_file):
	"""
    Execute SQL statements from a file.

    Args:
        conn (sqlite3.Connection): Database connection
        sql_file (str): Path to SQL file


    """
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
	"""
    Initialize database with schema and initial data.

    Executes SQL files in order:
    1. bank-schema.sql - Creates database structure
    2. bank-init.sql - Inserts initial data

  """
	init_files = ['database/bank-schema.sql', 'database/bank-init.sql']
	conn = sqlite3.connect(DB_PATH)
	if conn:
		_ = [execute_sql_file(conn, x) for x in init_files]
		conn.close()
	else:
		raise ValueError('Can not create connection to database')

def authenticate(username:int, password:str):
	"""
    Authenticate user credentials.

    Args:
        username (int): User's UUID
        password (str): User's password

    Returns:
        dict: User data {'id': int, 'uuid': str} if authenticated
        None: If authentication fails

  """
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
	"""
    Get current balance for a user.

    Args:
        user_id (int): User's ID

    Returns:
        int: User's current balance
  """
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
	"""
    Create new bank account.

    Args:
        uuid (str): User's UUID
        password (str): User's password

    Returns:
        dict: New account data {'id': int, 'uuid': str, 'balance': int}
  """
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
	"""
    Delete user account.

    Args:
        user_id (int): User's ID to delete
  """
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
	"""
    Transfer money between accounts.

    Performs an atomic transaction to:
    1. Verify receiver exists
    2. Check sufficient funds
    3. Update both account balances

    Args:
        id_from (int): Sender's account ID
        uuid_to (str): Receiver's UUID
        amount (int): Amount to transfer
  """
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
