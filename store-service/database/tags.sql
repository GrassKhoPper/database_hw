CREATE TABLE tags(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE game_tags (
  gameid INTEGER,
  tagid  INTEGER,
  PRIMARY KEY(gameid, tagid),

  FOREIGN KEY(gameid) REFERENCES games(gameid),
  FOREIGN KEY(tagid ) REFERENCES tags (tagid )
);

