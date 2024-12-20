"""
User class module for GameHub Store.

"""

import hashlib
import re

class User():
	"""
    Represents a user account in the GameHub store.

    Attributes:
        name (str): Username
        phash (str): MD5 hash of user's password
        balance (int): User's account balance
        regexp (str): Regular expression for valid username characters
        max_pass_length (int): Maximum allowed password length
        min_pass_length (int): Minimum required password length
        max_name_length (int): Maximum allowed username length
        min_name_length (int): Minimum required username length
  """
	name : str
	phash: str
	balance: int
	regexp = r"^[a-zA-Z0-9_]+$"
	max_pass_length = 32
	min_pass_length = 4
	max_name_length = 32
	min_name_length = 1

	def __init__(self, name:str, password:str, repassword:str = None):
		"""
        Initialize a new User instance with validation.

        Args:
            name (str): Desired username
            password (str): User's password
            repassword (str, optional): Password confirmation for new accounts
      """
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
