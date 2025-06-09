import os
import base64

from flask import Flask

from bank.routes.routes import routes_blueprint

app = Flask(__name__)
app.register_blueprint(routes_blueprint)
app.secret_key = os.environ.get('SECRET_KEY', base64.b64encode(os.urandom(24)))

@app.errorhandler(404)
def page_not_found(e):
	return str(e)

# run flask application
if __name__ == '__main__':
	ssl_context = ('bank.crt', 'bank.key')
	app.run('0.0.0.0', port=5001, debug=True, ssl_context=ssl_context)
