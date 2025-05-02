COPY users (id, password_hash, name, balance) 
FROM '/store-init-csvs/init-data-users.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ',');

COPY tags(id, name) 
FROM '/store-init-csvs/init-data-tags.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ',');

COPY studios(id, name) 
FROM '/store-init-csvs/init-data-studios.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

COPY games(id, name, price, description, brief, studio_id)
FROM '/store-init-csvs/init-data-games.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- generator can generate duplicates for this categories
-- COPY game_tags(game_id, tag_id)
-- FROM '/store-init-csvs/init-data-game-tags.csv'
-- WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- COPY purchases(id, owner_id, buyer_id, ts, game_id)
-- FROM '/store-init-csvs/init-data-purchases.csv'
-- WITH (FORMAT CSV, HEADER, DELIMITER ',', NULL 'NULL');

-- create temporary table for games pictures to transform csv
CREATE TEMP TABLE temp4gpictures (
    id INTEGER PRIMARY KEY,
    name TEXT,
    game_id INTEGER,
    img_type TEXT,
    img_fmt TEXT,
    img TEXT
);

COPY temp4gpictures 
FROM '/store-init-csvs/init-games-pictures.csv' 
WITH (FORMAT CSV, HEADER);

INSERT INTO games_pictures (id, name, game_id, img_type, img_fmt)
SELECT
    s.id,
    s.id::TEXT || 'g.' || s.img_fmt as name,
    s.game_id,
    s.img_type,
    s.img_fmt
FROM
    temp4gpictures s
ON CONFLICT (id) DO NOTHING;

DROP TABLE temp4gpictures;
-- end of copy games pictures

-- create temporary table for profile pictures to transform csv
CREATE TEMP TABLE temp4ppictures (
  id INTEGER PRIMARY KEY,
  name TEXT,
  user_id INTEGER,
  img_fmt TEXT,
  img TEXT
);

COPY temp4ppictures
FROM '/store-init-csvs/init-profile-pictures.csv'
WITH (FORMAT CSV, HEADER);

INSERT INTO profiles_pictures (id, name, user_id, img_fmt)
SELECT
  s.id,
  s.id::TEXT || 'p.' || s.img_fmt as name,
  s.user_id,
  s.img_fmt
FROM
  temp4ppictures s
ON CONFLICT (id) DO NOTHING;

DROP TABLE temp4ppictures;
-- end of copy profile pictures
