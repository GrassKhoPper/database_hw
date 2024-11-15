CREATE TABLE purchases(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  gameid INTEGER NOY NULL,

  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (gameid) REFERENCES games(gameid)
);

