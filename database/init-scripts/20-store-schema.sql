CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    balance INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS studios (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price INTEGER NOT NULL,
    description TEXT NOT NULL,
    brief TEXT NOT NULL,
    studio_id INTEGER NOT NULL,

    FOREIGN KEY (studio_id) REFERENCES studios (id)
);

CREATE TABLE IF NOT EXISTS games_pictures (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    game_id INTEGER NOT NULL,
    img_type TEXT NOT NULL CHECK (
        img_type IN ('screenshot', 'icon', 'cover', 'profile')
    ),
    img_fmt TEXT NOT NULL CHECK (img_fmt IN ('jpg', 'ico', 'png')),

    -- mb UNIQUE ( gameid , img_type==icon ) 
    -- and UNIQUE ( gameid, img_type=cover )
    FOREIGN KEY (game_id) REFERENCES games (id)
);

CREATE TABLE IF NOT EXISTS profiles_pictures (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    img_fmt TEXT NOT NULL CHECK (img_fmt IN ('jpg', 'png')),

    UNIQUE (user_id, name),

    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    ts INTEGER, -- make it NULL if game not buyed yet but in cart already
    game_id INTEGER NOT NULL,

    FOREIGN KEY (owner_id) REFERENCES users (id),
    FOREIGN KEY (buyer_id) REFERENCES users (id),
    FOREIGN KEY (game_id) REFERENCES games (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_owner_game ON purchases (
    owner_id, game_id
);

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS game_tags (
    game_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (game_id, tag_id),

    FOREIGN KEY (game_id) REFERENCES games (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);
