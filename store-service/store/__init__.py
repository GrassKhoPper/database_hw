import os
import base64

from flask import Flask, render_template

from store.routes.routes import routes_blueprint, before_request
from store.database.db_api import init_database

# initial state of database
init_database()

app = Flask(__name__)

app.static_folder   = 'static'
app.template_folder = 'templates'
app.register_blueprint(routes_blueprint)
app.secret_key = os.environ.get('SECRET_KEY', base64.b64encode(os.urandom(24)))
app.before_request(before_request)

@app.errorhandler(404)
def page_not_found(e):
  return render_template(
    'Error.html', 
    error_code=404, 
    error_msg =f'Page not found: {e}'
  ), 404

@app.errorhandler(429)
def rate_limit_exceed(e):
  return render_template(
    'Error.html',
    error_code=429,
    error_msg =f'Too many request: {e}'
  ), 429

@app.errorhandler(500)
def internal_server_error(e):
  return render_template(
    'Error.html',
    error_code = 500,
    error_msg  = f'Internal server error: {e}'
  ), 500

@app.errorhandler(Exception)
def handle_exception(e):
  return render_template(
    'Error.html',
    error_code = 500,
    error_msg  = str(e)
  ), 500

