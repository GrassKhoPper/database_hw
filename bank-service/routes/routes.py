from functools import wraps

from flask import (
	Blueprint,
	jsonify,
	request,
	g
)

from database.db import (
	get_user_balance,
	add_account,
	delete_account,
	authenticate,
	transfer
)

routes_blueprint = Blueprint('routes', __name__)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		auth = request.authorization
		if not auth or not authenticate(auth.username, auth.password):
			return jsonify({'message': 'authenticate failed'}), 401
		g.user = authenticate(auth.username, auth.password)
		return f(*args, **kwargs)
	return decorated_function

@routes_blueprint.route('/api/balance', methods=['GET'])
@login_required
def get_balance():
	try:
		return jsonify({
			'balance' : get_user_balance(g.user['id']), 
			'uuid' : g.user['uuid'],
			'id' : g.user['id'] 
		})
	except ValueError as e:
		return jsonify({'error' : str(e)}), 404

@routes_blueprint.route('/api/add-account', methods=['POST'])
def add_bank_account():
	try:
		data = request.get_json()
		if 'uuid' not in data or 'password' not in data:
			return jsonify({'error': 'no uuid or password field'}), 402
		r = add_account(data['uuid'], data['password'])
		return jsonify(r), 200
	except ValueError as e:
		return jsonify({'error': str(e)}), 404

@routes_blueprint.route('/api/delete-account', methods=['POST'])
@login_required
def delete_bank_account():
	try:
		delete_account(g.user['id'])
		return jsonify({'status': 'ok'}), 200
	except ValueError as e:
		return jsonify({'error' : str(e)}), 404

@routes_blueprint.route('/api/transfer', methods=['POST'])
@login_required
def transfer_to_account():
	try:
		data = request.get_json()
		if 'uuid_to' not in data or 'amount' not in data:
			return jsonify({'error' : 'no field uuid_to ir amount in request'}), 402
		uuid_to, amount = data['uuid_to'], data['amount']
		transfer(g.user['id'], uuid_to, amount)
		return jsonify({'status' : 'ok'}), 200
	except ValueError as e:
		return jsonify({'error': str(e)}), 404
