from flask import Blueprint, render_template, request, session, redirect, url_for

from utility.Game import Game
from utility.User import User

from database.db_api import get_games_list, get_game_by_id, check_user, add_user

routes_blueprint = Blueprint('routes', __name__)

def is_user_logged_in()->bool:
	print(session)
	return 'user_id' in session

@routes_blueprint.route('/', methods=['GET'])
@routes_blueprint.route('/store', methods=['GET']) # post for the future(search)
def main_page():
	return render_template('Store.html', games=[Game(game) for game in get_games_list()])

@routes_blueprint.route('/game/<int:game_id>', methods=['GET'])
def open_game_page(game_id):
	print(get_game_by_id(game_id))
	return render_template('Game.html', game=Game(get_game_by_id(game_id)))

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
				print(vars(user))
				user_id = check_user(user)

				session['user_id'] = user_id
				print(f'login user_id:{user_id}')

				return redirect(url_for('routes.open_profile'))

			except ValueError as e:
				print(f'error in login:{e}')
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
	return redirect(url_for('routes.main_page'))

@routes_blueprint.route('/profile', methods=['GET'])
def open_profile():
	print(f'is user logged in:{is_user_logged_in()}')
	if not is_user_logged_in():
		redirect(url_for('routes.login_register'))
	return render_template('User.html')

@routes_blueprint.route('/cart', methods=['GET'])
def open_cart_page():
	return render_template('Cart.html')

@routes_blueprint.route('/library', methods=['GET'])
def open_library_page():
	return render_template('Library.html')


