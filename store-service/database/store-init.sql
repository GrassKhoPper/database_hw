INSERT OR IGNORE INTO users (
  id,
  password_hash,
  name
)
VALUES (
  1, 
  'ad34f0c08ff8f72d11b5550778353102', 
  'seregga'
);

INSERT OR IGNORE INTO studios (
  id,
  name
)
VALUES (
  1,
  'Valve corporation'
);

INSERT OR IGNORE INTO games (
  id,
  name,
  price,
  description,
  studio_id
)
VALUES (
  1, 
  'DotA 2', 
  0.0, 
  'Another Valve game...', 
  1
);

INSERT OR IGNORE INTO tags (
  id,
  name
) 
VALUES(1, 'MOBA');
INSERT OR IGNORE INTO tags (
  id,
  name
)
VALUES(2, 'BETA');

INSERT OR IGNORE INTO game_tags (
  game_id,
  tag_id
)
VALUES (
  1, 
  1
);
INSERT OR IGNORE INTO game_tags (
  game_id,
  tag_id
)
VALUES (
  1, 
  2
);

