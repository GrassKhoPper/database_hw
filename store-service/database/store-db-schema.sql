CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS studios(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  price REAL NOT NULL,
  description TEXT NOT NULL,
  studio_id INTEGER NOT NULL,

  FOREIGN KEY (studio_id) REFERENCES studios(id)
);

CREATE TABLE IF NOT EXISTS pictures (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  gameid INTEGER NOT NULL,
  img_type TEXT NOT NULL CHECK (img_type in ('screenshot', 'icon', 'cover')),
  img_fmt TEXT NOT NULL CHECK (img_fmt in ('jpg', 'ico', 'png')),

  -- mb UNIQUE ( gameid , img_type==icon ) and UNIQUE ( gameid, img_type=cover )
  FOREIGN KEY (gameid) REFERENCES games(id)
);

CREATE TABLE IF NOT EXISTS purchases(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER NOT NULL,
  buyer_id INTEGER NOT NULL,
  ts INTEGER,
  game_id INTEGER NOT NULL,

  FOREIGN KEY (owner_id) REFERENCES users(id),
  FOREIGN KEY (buyer_id) REFERENCES users(id),
  FOREIGN KEY (game_id)  REFERENCES games(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_owner_game ON purchases (owner_id, game_id);

CREATE TABLE IF NOT EXISTS tags(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS game_tags (
  game_id INTEGER NOT NULL,
  tag_id  INTEGER NOT NULL,
  PRIMARY KEY(game_id, tag_id),

  FOREIGN KEY(game_id) REFERENCES games(id),
  FOREIGN KEY( tag_id) REFERENCES tags (id)
);

