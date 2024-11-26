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
),
(
  2,
  'IDK.SOFTWARE'
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
  0.00,
  'Another Valve game...', 
  1
),
(
  2,
  'Board Game',
  20.00,
  'For D&D Lovers we are here to present our brand new board game!',
  2
);

INSERT OR IGNORE INTO tags (
  id,
  name
) 
VALUES 
(
  1, 
  'MOBA'
),
(
  2, 
  'BETA'
);

INSERT OR IGNORE INTO game_tags (
  game_id,
  tag_id
)
VALUES 
(
  1, 
  1
),
(
  1, 
  2
);

INSERT OR IGNORE INTO games_pictures (
  id,
  name,
  game_id,
  img_type,
  img_fmt
)
VALUES 
(
  1,
  'dota.jpg',
  1,
  'cover',
  'jpg'
),
(
  2,
  'dota.ico',
  1,
  'icon',
  'ico'
);

INSERT OR IGNORE INTO profiles_pictures (
  id,
  name,
  user_id,
  img_fmt
)
VALUES (
  1,
  'test_user.jpg',
  1,
  'jpg'
);

