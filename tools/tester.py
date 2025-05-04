import psycopg
import os

conn_params = {
	'host'    : '127.0.0.1',
	'port'    : os.getenv('DB_PORT'),
	'dbname'  : os.getenv('STORE_DB_NAME'),
	'user'    : os.getenv('STORE_DB_USER'),
	'password': os.getenv('STORE_DB_PSWD'),
	'row_factory': psycopg.rows.dict_row
}
print(conn_params)

try:
	db = psycopg.connect(**conn_params)
	db.autocommit = True
except psycopg.OperationalError as e:
	raise ValueError(f'Failed to connect to database: {e}')

game_id = 8

cursor = db.cursor()

cursor.execute("""
	SELECT g.*, s.name AS studio_name
	FROM games g
	JOIN studios s ON s.id = g.studio_id
	WHERE g.id = %s;
""", (game_id,))

data = cursor.fetchall()
print(data)

try:
		cursor.execute("""
			SELECT name, img_type, img_fmt
			FROM games_pictures 
			WHERE game_id = %s;
		""", (game_id,))
		data = cursor.fetchall()
		print(data)
except:
	print('e')

db.close()

