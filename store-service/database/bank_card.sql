CREATE TABLE bank_card(
  id INTEGER PRIMARY KEY AUATOINCREMENT,
  userid INTEGER NOT NULL,
  card_number TEXT NOT NULL,
  cvc TEXT NOT NULL,

  FOREIGN KEY (userid) REFERENCES users(userid)
);

