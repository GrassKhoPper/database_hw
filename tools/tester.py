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

cursor = db.cursor()

cursor.execute("""
			SELECT t.name
			FROM game_tags gt
			JOIN tags t ON gt.tag_id = t.id
			WHERE gt.game_id = %s;
		""", (game_id,))
		data = cursor.fetchall()
		tags = [tag['name'] for tag in data]
		return tags

try:
	cursor.execute(queue, params)
	data = cursor.fetchall()
	print(data)
except psycopg.OperationalError as e:
	print(f'sql execution error {e}')

db.close()

