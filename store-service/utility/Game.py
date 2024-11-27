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
		print(data)
		self.game_id= data['id']
		self.name   = data['name']
		self.price  = data['price']
		self.brief  = data['brief']
		self.description = data['description']

		if 'studio_name' in data:
			self.studio = data['studio_name']
		if 'tags' in data:
			self.tags   = data['tags'].split(',') if data['tags'] else []
		if 'pictures' in data:
			pic_data = data['pictures'].split(',') if data['pictures'] else []
			self.screenshots = []
			for pic in pic_data:
				info = pic.split(':')
				match info[1]:
					case 'cover':
						self.cover = info[0]
					case 'icon':
						self.icon = info[0]
					case 'screenshot':
						self.screenshots.append(info[0])

		print(vars(self))
