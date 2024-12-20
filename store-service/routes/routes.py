"""
Routes module for GameHub Store web application.

This module handles all route definitions and request processing for the game store,
including user authentication, game browsing, cart management, and library access.
"""

from flask import (
	Blueprint, 
	render_template, 
	request, 
	session, 
	redirect, 
	url_for
)

from utility.Game import Game
from utility.User import User

from database.db_api import ( 
	get_games_list, 
	get_game_info, 
	check_user, 
	add_user, 
	get_profile_picture, 
	get_user_games_in_library, 
	get_user_cart_games,
	remove_from_cart,
	buy_cart
)

routes_blueprint = Blueprint('routes', __name__)

def is_user_logged_in()->bool:
	"""
    Checks if user is currently logged into the system.

    Returns:
        bool: True if user is logged in (user_id in session), False otherwise
  """
	return 'user_id' in session

@routes_blueprint.route('/', methods=['GET'])
@routes_blueprint.route('/store', methods=['GET'])
def main_page():
	"""
    Renders main store page with list of available games.

    Returns:
        rendered template: Store page with list of games
  """
	games = get_games_list()
	return render_template('Store.html', games=[Game(game) for game in games])

@routes_blueprint.route('/game/<int:game_id>', methods=['GET'])
def open_game_page(game_id):
	"""
    Displays detailed page for a specific game.

    Args:
        game_id (int): Unique identifier of the game

    Returns:
        rendered template: Game details page
  """
	# print(get_game_by_id(game_id))
	return render_template('Game.html', game=Game(get_game_info(game_id)))

@routes_blueprint.route('/login', methods=['GET','POST'])
def login_register():
	"""
    Handles user login and registration.

    Processes both GET requests to display the login form and POST requests
    for login and registration submissions. Handles form validation and user creation.

    Returns:
        rendered template: Login page with potential error messages
        redirect: Profile page on successful login
  """
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
				user_id, balance = check_user(user)

				session['user_id'] = user_id
				session['balance'] = balance
				session['username']= username
				print(f'login user_id:{user_id}')

				return redirect(url_for('routes.open_profile'))

			except ValueError as e:
				# print(f'error in login:{e}')
				login_error = str(e)
				return render_template(
					'Login.html', 
					login_error=login_error, 
					register_error=login_error, 
					active_form='login'
				)

		elif 'reg_submit' in request.form:
			username   = request.form.get('reg_username')
			password   = request.form.get('reg_password')
			repassword = request.form.get('reg_repassword')
			try:
				user = User(username, password, repassword)
				add_user(user)
				return redirect(url_for('routes.login_register'))

			except ValueError as e:
				register_error = str(e)
				return render_template(
					'Login.html', 
					login_error=login_error, 
					register_error=register_error, 
					active_form='register'
				)

	return render_template('Login.html', active_form='login')

@routes_blueprint.route('/logout')
def logout():
	"""
    Handles user logout by clearing session data.

    Returns:
        redirect: Main store page
  """
	session.pop('user_id', None)
	return redirect(url_for('routes.main_page'))

@routes_blueprint.route('/profile', methods=['GET'])
def open_profile():
	"""
    Displays user profile page with account information.

    Requires authentication. Shows user details including balance
    and profile picture.

    Returns:
        rendered template: User profile page
        redirect: Login page if user is not authenticated
  """
	print(f'is user logged in:{is_user_logged_in()}')
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))

	pic = get_profile_picture(session['user_id'])
	return render_template(
		'User.html',
		username=session['username'], 
		balance=session['balance'],
		uid=session['user_id'], 
		upicture=pic
	)

@routes_blueprint.route('/cart', methods=['GET'])
def open_cart_page():
	"""
    Displays user's shopping cart with game items and total.

    Requires authentication. Calculates total price of items in cart.

    Returns:
        rendered template: Cart page with games and total
        redirect: Login page if user is not authenticated
  """
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))
	game_list, games = get_user_cart_games(session['user_id']), []
	total_sum = 0
	for game in game_list:
		t = Game(get_game_info(game['game_id']))
		total_sum += t.price
		games.append(t)
	return render_template('Cart.html', games=games, total=total_sum)

@routes_blueprint.route('/cart/pay', methods=['POST'])
def buy_cart_user():
	"""
    Processes purchase of all items in user's cart.

    Requires authentication. Verifies user has sufficient balance
    and processes transaction.

    Returns:
        redirect: Cart page after purchase attempt
        redirect: Login page if user is not authenticated
  """
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))
	games_list, total, games = get_user_cart_games(session['user_id']), 0, []
	games_list = [get_game_info(game['game_id']) for game in games_list]
	print([dict(x) for x in games_list])
	for game in games_list:
		total += game['price']
		games.append(game['id'])
	if  total <= session['balance']:
		try:
			buy_cart(session['user_id'], total, games)
			session['balance'] -= total
		except ValueError as e:
			print(f'error:{e}')
	return redirect(url_for('routes.open_cart_page'))

@routes_blueprint.route('/cart/remove/<int:game_id>', methods=['POST'])
def remove_game_from_user_cart(game_id:int):
	"""
    Removes specific game from user's cart.

    Args:
        game_id (int): ID of game to remove

    Returns:
        redirect: Cart page after removal
        redirect: Login page if user is not authenticated
	"""
	if not is_user_logged_in():
		return redirect('/login')
	try:
		remove_from_cart(session['user_id'], game_id)
	except ValueError as e:
		print(f'exception:{e}')
	return redirect(url_for('routes.open_cart_page'))

@routes_blueprint.route('/game-details/<int:game_id>')
def game_details(game_id:int):
	"""
    Displays detailed information for specific game.

    Args:
        game_id (int): ID of game to display

    Returns:
        rendered template: Game details page
  """
	print(game_id)

@routes_blueprint.route('/library', methods=['GET'])
def open_library_page():
	"""
    Displays user's game library with owned games.

    Requires authentication. Shows all games owned by user.

    Returns:
        rendered template: Library page with user's games
        redirect: Login page if user is not authenticated
   """
	if not is_user_logged_in():
		return redirect(url_for('routes.login_register'))

	user_games = get_user_games_in_library(session['user_id'])
	return render_template('Library.html', user_games=[Game(x) for x in user_games])
