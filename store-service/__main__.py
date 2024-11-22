from flask import Flask

from routes.routes import routes_blueprint
from database.db_api import init_database

import os

# initial state of database
init_database()

# configure flask app
app = Flask(__name__)
app.static_folder   = 'static'
app.template_folder = 'templates'
app.register_blueprint(routes_blueprint)

# run flask application
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

