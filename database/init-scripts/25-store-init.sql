-- init users
COPY users (id, password_hash, name, balance)
FROM '/store-init-csvs/init-data-users.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');

SELECT
    setval(
        pg_get_serial_sequence('users', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM users;
-- init tags
COPY tags (id, name)
FROM '/store-init-csvs/init-data-tags.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');
SELECT
    setval(
        pg_get_serial_sequence('tags', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM tags;
-- init studios
COPY studios (id, name)
FROM '/store-init-csvs/init-data-studios.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');

SELECT
    setval(
        pg_get_serial_sequence('studios', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM studios;
-- init games
COPY games (id, name, price, description, brief, studio_id)
FROM '/store-init-csvs/init-data-games.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');

SELECT
    setval(
        pg_get_serial_sequence('games', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM games;
-- init game_tags
COPY game_tags (game_id, tag_id)
FROM '/store-init-csvs/init-data-game-tags.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');
-- init purchases
COPY purchases (id, owner_id, buyer_id, ts, game_id)
FROM '/store-init-csvs/init-data-purchases.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',', NULL 'NULL');

SELECT
    setval(
        pg_get_serial_sequence('purchases', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM purchases;
-- create temporary table for games pictures to transform csv
CREATE TEMP TABLE IF NOT EXISTS temp4gpictures (
    id INTEGER PRIMARY KEY,
    name TEXT,
    game_id INTEGER,
    img_type TEXT,
    img_fmt TEXT,
    img TEXT
);

COPY temp4gpictures
FROM '/store-init-csvs/init-games-pictures.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');

INSERT INTO games_pictures (id, name, game_id, img_type, img_fmt)
SELECT
    s.id,
    s.id::TEXT || 'g.' || s.img_fmt AS picture_name,
    s.game_id,
    s.img_type,
    s.img_fmt
FROM
    temp4gpictures AS s
ON CONFLICT (id) DO NOTHING;
SELECT
    setval(
        pg_get_serial_sequence('games_pictures', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM games_pictures;

DROP TABLE temp4gpictures;
-- end of copy games pictures

-- create temporary table for profile pictures to transform csv
CREATE TEMP TABLE IF NOT EXISTS temp4ppictures (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER,
    img_fmt TEXT,
    img TEXT
);

COPY temp4ppictures
FROM '/store-init-csvs/init-profile-pictures.csv'
WITH (FORMAT csv, HEADER, DELIMITER ',');

INSERT INTO profiles_pictures (id, name, user_id, img_fmt)
SELECT
    s.id,
    s.id::TEXT || 'p.' || s.img_fmt AS profile_pic_name,
    s.user_id,
    s.img_fmt
FROM
    temp4ppictures AS s
ON CONFLICT (id) DO NOTHING;
SELECT
    setval(
        pg_get_serial_sequence('profiles_pictures', 'id'),
        coalesce(max(id), 0) + 1
    )
FROM profiles_pictures;

DROP TABLE temp4ppictures;

COMMIT;
-- end of copy profile pictures
