-- Table definitions for the tournament project.



CREATE TABLE player (id serial PRIMARY KEY, name text);

CREATE TABLE match (id int PRIMARY KEY, num_of_matches int, num_of_wins int);

CREATE VIEW player_match AS SELECT player.id, player.name, match.num_of_matches, match.num_of_wins FROM player LEFT JOIN match ON player.id = match.id;

