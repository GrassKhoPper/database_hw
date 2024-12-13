import hashlib
import re

class User():
	name : str
	phash: str
	balance: int
	regexp = r"^[a-zA-Z0-9_]+$"
	max_pass_length = 32
	min_pass_length = 4
	max_name_length = 32
	min_name_length = 1

	def __init__(self, name:str, password:str, repassword:str = None):
		if len(name) < User.min_name_length or len(name) > User.max_name_length :
			raise ValueError('Username length error: length must be',
										f'{User.min_name_length}-{User.max_name_length}')

		if len(password) < User.min_pass_length or len(name) > User.max_pass_length :
			raise ValueError('Password length error: length must be', 
										f'{User.min_pass_length}-{User.max_pass_length}')

		if not re.match(self.regexp, name):
			raise ValueError('Username must have only letters, numbers or _ symbol')

		self.name = name
		self.phash = hashlib.md5(password.encode()).hexdigest()

		if repassword:
			rphash = hashlib.md5(repassword.encode()).hexdigest()
			if rphash != self.phash:
				raise ValueError('Passwords does not matching')
