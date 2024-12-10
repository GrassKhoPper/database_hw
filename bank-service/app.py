from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

# run flask application
if __name__ == '__main__':
	app.run('0.0.0.0', port=5001, debug=True)
