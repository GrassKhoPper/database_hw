"""
Data Generator Module for GameHub Store

This module generates initial data for the GameHub store database in CSV format.
Generates users, studios, games, tags, purchases and associated images.

Constants:
    - USERS_COUNT (int): Number of users to generate
    - STUDIO_COUNT (int): Number of game studios
    - TAGS_COUNT (int): Number of game tags/categories
    - GAMES_COUNT (int): Number of games
    - MAX_SCREENSHOT_COUNT (int): Maximum screenshots per game
    - GAME_TAGS_COUNT (int): Number of game-tag associations
    - PURCHASES_COUNT (int): Number of game purchases

Output Files:
    - init-data-users.csv: User accounts data
    - init-data-studios.csv: Game studios data
    - init-data-games.csv: Games information
    - init-data-tags.csv: Game categories/tags
    - init-data-game-tags.csv: Game-tag associations
    - init-data-purchases.csv: Game purchase records
    - init-profile-pictures.csv: User profile images
    - init-games-pictures.csv: Game-related images (covers, icons, screenshots)
"""

import csv
import hashlib
import random
from PIL import Image, ImageFont, ImageDraw
import io
import base64

USERS_COUNT  = 100
init_users_csv  = './store-service/database/csv-init/init-data-users.csv'
users_headers    = ['id', 'password_hash', 'name', 'balance']
init_profile_pictures_csv = './store-service/database/csv-init/init-profile-pictures.csv'
profile_pictures_headers = ['id', 'name', 'user_id', 'img_fmt', 'img']

STUDIO_COUNT = 10
init_studio_csv = './store-service/database/csv-init/init-data-studios.csv'
studios_headers = ['id', 'name']

TAGS_COUNT = 20
init_tags_csv = './store-service/database/csv-init/init-data-tags.csv'
tags_headers  = ['id', 'name']

GAMES_COUNT, MAX_SCREENSHOT_COUNT = 100, 8
init_games_csv = './store-service/database/csv-init/init-data-games.csv'
games_headers  = ['id', 'name', 'price', 'description', 'brief', 'studio_id']
init_games_pictures_csv = './store-service/database/csv-init/init-games-pictures.csv'
games_pictures_headers = ['id', 'name', 'game_id', 'img_type', 'img_fmt', 'img']

GAME_TAGS_COUNT = 1000
init_game_tags_csv = './store-service/database/csv-init/init-data-game-tags.csv'
game_tags_headers  = ['game_id', 'tag_id']

PURCHASES_COUNT = 1000
init_purchases_csv = './store-service/database/csv-init/init-data-purchases.csv'
purchases_headers = ['id', 'owner_id', 'buyer_id', 'ts', 'game_id']

def generate_user(idx:int):
	"""
    Generate user data record.

    Args:
        idx (int): User identifier

    Returns:
        list: [id, password_hash, username, balance]
    """
	return [
		idx,
		hashlib.md5(f'username{idx}'.encode()).hexdigest(),
		f'username{idx}',
		round(random.uniform(0, 10000))
	]

def generate_studio(idx:int):
	"""
    Generate game studio record.

    Args:
        idx (int): Studio identifier

    Returns:
        list: [id, studio_name]
    """
	return [idx, f'studio{idx}']

def generate_tag(idx:int):
	"""
    Generate game tag record.

    Args:
        idx (int): Tag identifier

    Returns:
        list: [id, tag_name]
    """
	return [idx, f'tag{idx}']

def generate_game_tag(idx:int):
	"""
    Generate game-tag association record.

    Args:
        idx (int): Association identifier

    Returns:
        list: [game_id, tag_id]
    """
	return [
		round(random.uniform(1, GAMES_COUNT)),
		round(random.uniform(1,  TAGS_COUNT))
	]

def generate_game(idx:int):
	"""
    Generate game record.

    Args:
        idx (int): Game identifier

    Returns:
        list: [id, name, price, description, brief, studio_id]
    """
	return [
		idx,
		f'game{idx}',
		round(random.uniform(0, 10000)),
		f'<p>Description for game{idx}</p>',
		f'Brief for game{idx}',
		round(random.uniform(1, STUDIO_COUNT))
	]

def generate_purchase(idx:int):
	"""
    Generate game purchase record.

    Args:
        idx (int): Purchase identifier

    Returns:
        list: [id, owner_id, buyer_id, timestamp, game_id]
    """
	return [
		idx,
		round(random.uniform(1, USERS_COUNT)),
		round(random.uniform(1, USERS_COUNT)),
		'NULL' if round(random.uniform(0,2)) == 0 else round(random.uniform(1, 100000)),
		round(random.uniform(1, GAMES_COUNT)) 
	]

def create_image_with_text(text:str):
	"""
    Generate PNG image with centered text.

    Args:
        text (str): Text to render on image

    Returns:
        str: Base64 encoded PNG image data
    """
	WIDTH, HEIGHT = 250, 250
	img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype('FreeMono', 30) # replace with your font
	text_width = draw.textlength(text, font=font)
	try:
		ascent, descent = font.getmetrics()
		text_height = ascent + descent
	except AttributeError:
		text_height = font.getsize(text)[1] 
	x = (WIDTH  -  text_width) // 2
	y = (HEIGHT - text_height) // 2
	draw.text((x, y), text, font=font, fill=(0, 0, 0))

	buffered = io.BytesIO()
	img.save(buffered, format='PNG')
	image = base64.b64encode(buffered.getvalue()).decode()
	return image

def generate_profile_picture(idx:int):
	"""
    Generate user profile picture
	    Args:
        idx (int): Picture identifier

    Returns:
        list: [id, filename, user_id, format, image_data]
    """
	
	return [
		idx, 
		f'{idx}.png',
		idx,
		'png',
		create_image_with_text(f'u{idx}')
	]

def generate_games_pictures(count=GAMES_COUNT, csv_out=init_games_pictures_csv, headers=games_pictures_headers):
	"""
    Generate game-related images (cover, icon, screenshots).
    Writes records directly to CSV file.
    """
	with open(csv_out, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(headers)
		counter = 1
		for idx in range(1, count + 1):
			writer.writerow([
				counter, 
		 		f'cover{idx}.png',
				 idx,
				 'cover',
				 'png',
				 create_image_with_text(f'cover{idx}')
			])
			counter += 1
			writer.writerow([
				counter, 
				f'icon{idx}.png',
				idx,
				'icon',
				'png',
				create_image_with_text(f'icon{idx}')
			])
			counter += 1
			screen_count = round(random.uniform(0, MAX_SCREENSHOT_COUNT))
			for jdx in range(1, screen_count + 1):
				writer.writerow([
					counter,
					f'screen{jdx}.png',
					idx,
					'screenshot',
					'png',
					create_image_with_text(f'screen{jdx}')
				])
				counter += 1

def generate_file(
	count: int, 
	headers: list[str],
	csv_out: str, 
	datagen
):
	"""
    Generate CSV file with data records.

    Args:
        count (int): Number of records to generate
        headers (list[str]): CSV column headers
        csv_out (str): Output file path
        datagen: Function to generate data records
    """
	data = [datagen(idx) for idx in range(1, count+1)]
	with open(csv_out, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(headers)
		writer.writerows(data)

try:
	generate_file(count=USERS_COUNT, csv_out=init_users_csv, headers=users_headers, datagen=generate_user)
	print('Users csv file generated!')
	generate_file(count=STUDIO_COUNT, csv_out=init_studio_csv, headers=studios_headers, datagen=generate_studio)
	print('Studios csv file generated!')
	generate_file(count=GAMES_COUNT, csv_out=init_games_csv, headers=games_headers, datagen=generate_game)
	print('Games csv file generated!')
	generate_file(count=TAGS_COUNT, csv_out=init_tags_csv, headers=tags_headers, datagen=generate_tag)
	print('Tags csv file generated!')
	generate_file(count=GAME_TAGS_COUNT, csv_out=init_game_tags_csv, headers=game_tags_headers, datagen=generate_game_tag)
	print('Game tags csv generated!')
	generate_file(count=PURCHASES_COUNT, csv_out=init_purchases_csv, headers=purchases_headers, datagen=generate_purchase)
	print('Purchases csv file generated!')
	generate_file(count=USERS_COUNT, csv_out=init_profile_pictures_csv, headers=profile_pictures_headers, datagen=generate_profile_picture)
	print('Profile pictures csv generated!')
	generate_games_pictures()
	print('Games pictures csv generated!')

except Exception as e:
	print(f'Error: {e}')