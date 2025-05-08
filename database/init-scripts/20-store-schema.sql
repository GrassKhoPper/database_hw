CREATE SCHEMA IF NOT EXISTS store;

CREATE TABLE IF NOT EXISTS store.users (
    id SERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    balance INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS store.studios (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS store.games (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price INTEGER NOT NULL,
    description TEXT NOT NULL,
    brief TEXT NOT NULL,
    studio_id INTEGER NOT NULL,

    FOREIGN KEY (studio_id) REFERENCES store.studios (id)
);

CREATE TABLE IF NOT EXISTS store.games_pictures (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    game_id INTEGER NOT NULL,
    img_type TEXT NOT NULL CHECK (
        img_type IN ('screenshot', 'icon', 'cover', 'profile')
    ),
    img_fmt TEXT NOT NULL CHECK (img_fmt IN ('jpg', 'ico', 'png')),

    -- mb UNIQUE ( gameid , img_type==icon ) 
    -- and UNIQUE ( gameid, img_type=cover )
    FOREIGN KEY (game_id) REFERENCES store.games (id)
);

CREATE TABLE IF NOT EXISTS store.profiles_pictures (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    img_fmt TEXT NOT NULL CHECK (img_fmt IN ('jpg', 'png')),

    UNIQUE (user_id, name),

    FOREIGN KEY (user_id) REFERENCES store.users (id)
);

CREATE TABLE IF NOT EXISTS store.purchases (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    ts INTEGER, -- make it NULL if game not buyed yet but in cart already
    game_id INTEGER NOT NULL,

    FOREIGN KEY (owner_id) REFERENCES store.users (id),
    FOREIGN KEY (buyer_id) REFERENCES store.users (id),
    FOREIGN KEY (game_id) REFERENCES store.games (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_owner_game ON store.purchases (
    owner_id, game_id
);

CREATE TABLE IF NOT EXISTS store.tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS store.game_tags (
    game_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (game_id, tag_id),

    FOREIGN KEY (game_id) REFERENCES store.games (id),
    FOREIGN KEY (tag_id) REFERENCES store.tags (id)
);
