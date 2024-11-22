from flask import Blueprint, render_template

from store.database.db_api import *

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
@routes_blueprint.route('/store')
def main_page():
    return render_template('Store.html')

@routes_blueprint.route('/add_item', methods=['POST'])
def add_item_route():
    return redirect(url_for('routes.main_page'))

@routes_blueprint.route('/profile')
def open_profile_page():
    return render_template('User.html')

@routes_blueprint.route('/game')
def open_game_page():
    return render_template('Game.html')
