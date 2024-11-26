class Game:
	name: str
	price: float
	cover: str
	description: str
	screenshots: list[str]
	tags: list[str]
	stuido: str
	game_id: int

	def __init__(self, data:dict):
		self.game_id= data['id']
		self.name   = data['name']
		self.price  = data['price']
		self.stuido = data['studio_id']
		self.description = data['description']
		self.cover = 'dota.jpg'
