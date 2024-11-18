from flask import Flask
from routes.routes import routes_blueprint
import os

app = Flask(__name__)
app.register_blueprint(routes_blueprint)
app.static_folder   = os.environ.get('STATIC_DIR', 'static')
app.template_folder = os.environ.get('TEMPLATE_DIR', 'template')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

