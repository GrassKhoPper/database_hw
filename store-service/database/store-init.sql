INSERT OR IGNORE INTO users VALUES(1, 'ad34f0c08ff8f72d11b5550778353102', 'seregga');

INSERT OR IGNORE INTO studios VALUES(1, 'Valve corporation');

INSERT OR IGNORE INTO games VALUES(1, 'DotA 2', 0.0, 'Another Valve game...', 1);

INSERT OR IGNORE INTO tags VALUES(1, 'MOBA');
INSERT OR IGNORE INTO tags VALUES(2, 'TOXIC');

INSERT OR IGNORE INTO game_tags VALUES(1, 1);
INSERT OR IGNORE INTO game_tags VALUES(1, 2);
