from flask import Flask, Cache

from routes.routes import routes_blueprint
from database.db_api import init_database

import os
import base64

# initial state of database
init_database()

# configure flask app
config = {
	'DEBUG' : True,
  'CACHE_TYPE' : 'SimpleCache',
  'CACHE_DEFAULT_TIMEOUT': 300
}

app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)

app.static_folder   = 'static'
app.template_folder = 'templates'
app.register_blueprint(routes_blueprint)
app.secret_key = os.environ.get('SECRET_KEY', base64.b64encode(os.urandom(24)))

# run flask application
if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)

