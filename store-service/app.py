import os
import base64

from flask import Flask

from routes.routes import routes_blueprint
from database.db_api import init_database

# initial state of database
init_database()

app = Flask(__name__)

app.static_folder   = 'static'
app.template_folder = 'templates'
app.register_blueprint(routes_blueprint)
app.secret_key = os.environ.get('SECRET_KEY', base64.b64encode(os.urandom(24)))

# run flask application
if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)
