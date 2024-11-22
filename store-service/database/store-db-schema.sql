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
  studioid INTEGER,

  FOREIGN KEY (studioid) REFERENCES studios(studioid)
);

CREATE TABLE IF NOT EXISTS bank_card(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  card_number TEXT NOT NULL,
  cvc TEXT NOT NULL,

  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE IF NOT EXISTS cart(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER,
  gameid INTEGER,
  
  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (gameid) REFERENCES games(gameid)
);

CREATE TABLE IF NOT EXISTS purchases(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  gameid INTEGER NOY NULL,

  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (gameid) REFERENCES games(gameid)
);

CREATE TABLE IF NOT EXISTS tags(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS game_tags (
  gameid INTEGER,
  tagid  INTEGER,
  PRIMARY KEY(gameid, tagid),

  FOREIGN KEY(gameid) REFERENCES games(gameid),
  FOREIGN KEY(tagid ) REFERENCES tags (tagid )
);

