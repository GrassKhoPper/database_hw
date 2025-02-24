class Game:
	name: str
	price: float
	description: str
	brief: str
	game_id: int
	
	cover: str
	screenshots: list[str]
	icon: str

	tags: list[str]
	studio: str

	def __init__(self, data:dict):
		self.game_id= data['id']
		self.name   = data['name']
		self.price  = data['price']
		self.brief  = data['brief']
		self.description = data['description']

		if 'studio_name' in data:
			self.studio = data['studio_name']
		if 'tags' in data:
			self.tags   = data['tags'] if data['tags'] else []
		if 'pictures' in data:
			pic_data = data['pictures'] if data['pictures'] else []
			self.screenshots = []
			for pic in pic_data:
				match pic['img_type']:
					case 'cover':
						self.cover = pic['name']
					case 'icon':
						self.icon = pic['name']
					case 'screenshot':
						self.screenshots.append(pic['name'])
