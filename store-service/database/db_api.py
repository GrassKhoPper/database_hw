
"""
Database operations module for the game store. This module provides functions for database initialization and data retrieval operations.
"""

import sqlite3
import os
from flask import g

DB_PATH = os.environ.get('DB_PATH', '/var/store-db/store.sql3.db')

def create_connection(db_file):
	"""
    Create a database connection to the SQLite database.

    Args:
        db_file (str): Path to the SQLite database file

    Returns:
        sqlite3.Connection: Database connection object or None if connection fails
    """
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(f'Can not create connection to database: {e}')
	return conn

def execute_sql_file(conn, sql_file):
	"""
    Execute SQL commands from a file.

    Args:
        conn (sqlite3.Connection): Database connection object
        sql_file (str): Path to the SQL file to execute

    Returns:
        None
    """
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
	"""
    Initialize the database with schema and initial data.
    
    Executes SQL files containing schema and initial data definitions.
    
    Returns:
        None
    """
	db_path = DB_PATH
	init_files = ['database/store-db-schema.sql', 'database/store-init.sql']
	conn = create_connection(db_path)
	if conn:
		[execute_sql_file(conn, x) for x in init_files]
		conn.close()
	else:
		print('Can not create connection to database')

def get_db():
	"""
    Get or create database connection for the current context.

    Returns:
        sqlite3.Connection
    """
	if 'db' not in g:
		g.db = sqlite3.connect(DB_PATH)
		g.db.isolation_level = None
		g.db.row_factory = sqlite3.Row
	return g.db

def get_games_list()->list[dict]:
	"""
    Retrieve list of all games with related information.

    Returns:
        list[dict]: List of dictionaries containing game information including:
        None if there's an error
    """
	db = get_db()
	cursor = db.cursor()
	try:
		cursor.execute("""
			SELECT g.*, s.name AS studio_name,
      	(SELECT p.name FROM games_pictures p WHERE p.game_id = g.id AND p.img_type = 'cover') AS cover_image,
      	GROUP_CONCAT(DISTINCT p.name || ':' || p.img_type || ':' || p.img_fmt) AS pictures
			FROM games g
			JOIN studios s ON g.studio_id = s.id
			LEFT JOIN game_tags gt ON g.id = gt.game_id
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
	"""
    Retrieve detailed information about a specific game.

    Args:
        game_id (int): The ID of the game to retrieve

    Returns:
        dict: Dictionary containing game information including:
        None if game not found or there's an error
    """
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

