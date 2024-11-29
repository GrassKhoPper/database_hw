store-service
=============
Store-service is the service responsible for managing the game store and related operations.

database
________

db_api.py
~~~~~~~~~

.. automodule:: db_api
   :members:
   :undoc-members:

store-db-schema.sql
~~~~~~~~~~~~~~~~~~~
You can view the database schema here:
https://github.com/GrassKhoPper/database_hw/blob/master/schema.png

store-init.sql
~~~~~~~~~~~~~~~

Database initialization

routes
______

routes.py
~~~~~~~~~
.. automodule:: routes
   :members:
   :undoc-members:

utility
________

DescriptionRedactor.py
~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: DescriptionRedactor
   :members:
   :undoc-members:

Game.py
~~~~~~~~~
Game class module with all its associated attributes and functionality

 class Game:
	A class representing a game in the store.

    Attributes:
        - name (str): The name of the game

        - price (float): The price of the game

        - description (str): Detailed description of the game

        - game_id (int): Unique identifier for the game

        - cover (str): Filename of the game's cover image

        - screenshots (list[str]): List of screenshot image filenames

        - icon (str): Filename of the game's icon

        - tags (list[str]): List of tags associated with the game

        - studio (str): Name of the game development studio
Game. __init__(self, data:dict):
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
templates
__________

The templates directory contains all HTML templates used in the game store.

- Authorisation.html
~~~~~~~~~~~~~~~~~~~~

- Cart.html
~~~~~~~~~~~~~

- Game.html
~~~~~~~~~~~~~

- Library.html
~~~~~~~~~~~~~~~

- Store.html
~~~~~~~~~~~~~

- User.html
~~~~~~~~~~~~



app.py
______

Main module for the Game Store.

It handles application configuration, database initialization,
and starts the web server.


  
