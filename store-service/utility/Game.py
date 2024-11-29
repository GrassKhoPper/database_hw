"""
Game class module with all its associated attributes and functionality

"""
class Game:
	"""
	A class representing a game in the store.

    Attributes:
        name (str): The name of the game
        price (float): The price of the game
        description (str): Detailed description of the game
        game_id (int): Unique identifier for the game
        cover (str): Filename of the game's cover image
        screenshots (list[str]): List of screenshot image filenames
        icon (str): Filename of the game's icon
        tags (list[str]): List of tags associated with the game
        studio (str): Name of the game development studio

    """
	name: str
	price: float
	description: str
	game_id: int
	
	cover: str
	screenshots: list[str]
	icon: str

	tags: list[str]
	studio: str

	def __init__(self, data:dict):
		"""
        Initialize a new Game instance.

        Args:
            data (dict): Dictionary containing game data with the following keys:
                - id: Game identifier
                - name: Game name
                - price: Game price
                - description: Game description
                - studio_name (optional): Development studio name
                - tags (optional): String of game tags
                - pictures (optional): String of picture data
        """
		print(data)
		self.game_id= data['id']
		self.name   = data['name']
		self.price  = data['price']
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
