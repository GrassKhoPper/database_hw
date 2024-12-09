from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from utility.Game import Game
from utility.User import User

from database.db_api import ( 
	get_games_list, 
	get_game_info, 
	check_user, 
	add_user, 
	get_profile_picture, 
	get_user_games_in_library, 
	get_user_games,
	get_pictures_by_game_id,
	get_tags_by_game_id
)

routes_blueprint = Blueprint('routes', __name__)

def is_user_logged_in()->bool:
	return 'user_id' in session

@routes_blueprint.route('/', methods=['GET'])
@routes_blueprint.route('/store', methods=['GET']) # post for the future(search)
def main_page():
	print(get_user_games(1))
	# return render_template('Store.html', games=[])
	games = get_games_list()
	print([dict(x) for x in games])
	
	return render_template('Store.html', games=[Game(game) for game in games])

@routes_blueprint.route('/game/<int:game_id>', methods=['GET'])
def open_game_page(game_id):
	# print(get_game_by_id(game_id))
	return render_template('Game.html', game=Game(get_game_info(game_id)))

@routes_blueprint.route('/login', methods=['GET','POST'])
def login_register():
	if is_user_logged_in():
		return redirect(url_for('routes.open_profile'))

	login_error = None
	register_error = None

	if request.method == 'POST':
		if 'login_submit' in request.form:
			username = request.form.get('login_username')
			password = request.form.get('login_password')
			try:
				user = User(username, password)
				# print(vars(user))
				user_id = check_user(user)

				session['user_id'] = user_id
				print(f'login user_id:{user_id}')

				return redirect(url_for('routes.open_profile'))

			except ValueError as e:
				# print(f'error in login:{e}')
				login_error = str(e)
				return render_template('Login.html', login_error=login_error, register_error=login_error, active_form='login')

		elif 'reg_submit' in request.form:
			username   = request.form.get('reg_username')
			password   = request.form.get('reg_password')
			repassword = request.form.get('reg_repassword')
			try:
				user = User(username, password, repassword)
				add_user(user)
				user_id = check_user(user)
				session['user_id'] = user_id
				return redirect(url_for('routes.open_profile'))

			except ValueError as e:
				register_error = str(e)
				return render_template('Login.html', login_error=login_error, register_error=register_error, active_form='register')

	return render_template('Login.html', active_form='login')

@routes_blueprint.route('/logout')
def logout():
	session.pop('user_id', None)
	print('I AM HERE PLEASE HELP ME TO BREATH')
	return redirect(url_for('routes.main_page'))

@routes_blueprint.route('/profile', methods=['GET'])
def open_profile():
	print(f'is user logged in:{is_user_logged_in()}')
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))

	pic = get_profile_picture(session['user_id'])
	return render_template('User.html', uid=session['user_id'], upicture=pic)

@routes_blueprint.route('/cart', methods=['GET'])
def open_cart_page():
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))
	# game_list = get_cart_games_for_user(session['user_id'])
	# print(game_list)
	return render_template('Cart.html')#, games=game_list)

@routes_blueprint.route('/game-details/<int:game_id>')
def game_details(game_id:int):
	pass

@routes_blueprint.route('/library', methods=['GET'])
def open_library_page():
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))

	user_games = get_user_games_in_library(session['user_id'])
	# user_games = [jsonify(game.__dict__) for game in user_games]
	# print(user_games)
	return render_template('Library.html', user_games=[Game(x) for x in user_games])
