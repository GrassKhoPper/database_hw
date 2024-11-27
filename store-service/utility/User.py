# from flask_login import UserMixin
import hashlib

class User():  # Наследуемся от UserMixin
	name : str
	phash: str

	def __init__(self, name:str, password:str, repassword:str = None):
		self.name = name
		self.phash = hashlib.md5(password.encode()).hexdigest()
		if repassword:
			rphash = hashlib.md5(repassword.encode()).hexdigest()
			if rphash != self.phash:
				raise ValueError('Passwords does not matching')
