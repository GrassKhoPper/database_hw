COPY users (id, password_hash, name, balance) 
FROM '/store-init-csvs/init-data-users.csv' 
DELIMITER ',' CSV HEADER;

COPY tags(id, name) 
FROM '/store-init-csvs/init-data-tags.csv' 
DELIMITER ',' CSV HEADER;

COPY studios(id, name) 
FROM '/store-init-csvs/init-data-studios.csv'
DELIMITER ',' CSV HEADER;

COPY games(id, name, price, description, brief, studio_id)
FROM '/store-init-csvs/init-data-games.csv'
DELIMITER ',' CSV HEADER;

COPY game_tags(game_id, tag_id)
FROM '/store-init-csvs/init-data-game-tags.csv'
DELIMITER ',' CSV HEADER;

