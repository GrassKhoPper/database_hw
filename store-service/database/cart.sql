CREATE TABLE cart(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER,
  gameid INTEGER,
  
  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (gameid) REFERENCES games(gameid)
);

