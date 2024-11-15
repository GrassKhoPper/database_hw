CREATE TABLE games (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  price REAL NOT NULL,
  description TEXT NOT NULL,
  studioid INTEGER,

  FOREIGN KEY (studioid) REFERENCES studios(studioid)
);

