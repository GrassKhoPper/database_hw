"""
Module routes defines the routes and their corresponding view functions.
It handles page rendering and navigation.

"""
from flask import Blueprint, render_template, redirect, url_for

from utility.Game import Game
from database.db_api import get_games_list, get_game_by_id

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
@routes_blueprint.route('/store')
def main_page():
    """
    Render the main store page.

    This route handles both the root ('/') and '/store' path.
    It displays a list of all available games.

    Returns:
        str:  Rendered HTML template for the store page with list of games
    """
    return render_template('Store.html', games=[Game(game) for game in get_games_list()])

@routes_blueprint.route('/profile')
def open_profile_page():
    """
    Render the user profile page.

    Returns:
        Rendered HTML template for the user profile page
    """
    return render_template('User.html')

@routes_blueprint.route('/game/<int:game_id>')
def open_game_page(game_id):
    """
    Render the detailed game page for a specific game.

    Args:
        game_id (int): The ID of the game to display

    Returns:
        str: Rendered HTML template for the specific game page
    """
    print(get_game_by_id(game_id))
    return render_template('Game.html', game=Game(get_game_by_id(game_id)))

@routes_blueprint.route('/auth')
def open_auth_page():
    """
    Render the authentication page.

    This page handles user login and registration.

    Returns:
        str: Rendered HTML template for the authentication page
    """
    return render_template('Authorisation.html')

@routes_blueprint.route('/cart')
def open_cart_page():
    """
    Render the shopping cart page.

    Displays the user's current shopping cart contents.

    Returns:
        str: Rendered HTML template for the shopping cart page
    """
    return render_template('Cart.html')

@routes_blueprint.route('/library')
def open_library_page():
    """
    Render the game library page.

    Displays all games owned by the current user.

    Returns:
        str: Rendered HTML template for the library page
    """
    return render_template('Library.html')

