from flask import Blueprint, render_template
# from ..services.services import *

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
@routes_blueprint.route('/store')
def main_page():
    return render_template('Store.html',
                           static_folder='../static',
                           templates_folder='../templates')

@routes_blueprint.route('/add_item', methods=['POST'])
def add_item_route():
    return redirect(url_for('routes.main_page'))
