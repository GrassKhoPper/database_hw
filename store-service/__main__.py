from flask import Flask

from routes.routes import routes_blueprint
from database.db_api import *

import os

init_database()

app = Flask(__name__)
app.static_folder   = os.environ.get('STATIC_DIR', 'static')
app.template_folder = os.environ.get('TEMPLATE_DIR', 'templates')
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

