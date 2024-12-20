"""
Game class module for GameHub Store.
"""

class Game:
	"""
    Represents a game in the store with all its associated data.

    Attributes:
        name (str): Title of the game
        price (float): Price of the game in currency units
        description (str): Full description of the game
        brief (str): Short description/summary of the game
        game_id (int): Unique identifier for the game
        cover (str): Filename of the game's cover image
        screenshots (list[str]): List of screenshot image filenames
        icon (str): Filename of the game's icon image
        tags (list[str]): List of tags/categories associated with the game
        studio (str): Name of the game development studio
    """
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
		"""
    Initializes a Game instance from dictionary data.

    Parameters:
        data (dict) - 
          Dictionary containing game data with the following keys:
            - id (int): Game identifier
            - name (str): Game title 
            - price (float): Game price
            - brief (str): Brief description
            - description (str): Full description
            - studio_name (str, optional): Developer studio name
            - tags (list[str], optional): Game categories/tags
            - pictures (list[dict], optional): Game images data containing:
                - img_type (str): Type of image ('cover', 'icon', 'screenshot')
                - name (str): Image filename
    """
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
