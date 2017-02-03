-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE player (id SERIAL PRIMARY KEY, name text);

CREATE TABLE match (id INT PRIMARY KEY REFERENCES player(id) ON DELETE CASCADE, num_of_matches INT, num_of_wins INT);

CREATE VIEW player_match AS SELECT player.id, player.name, match.num_of_matches, match.num_of_wins FROM player LEFT JOIN match ON player.id = match.id;

