-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Store player data
CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);


-- Store match data
-- When the draw flag is set to true, winner refers to player 1 and loser refers
-- to player 2 in the drawn match
-- When loser is null, the match is a bye/walkover with win awarded to winner
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES players (id) NOT NULL,
  loser INTEGER REFERENCES players (id),
  draw_flag BOOLEAN DEFAULT FALSE,
  CHECK (winner != loser)
);

-- Match view that shows players' name
CREATE VIEW view_matches_all AS
  SELECT id AS match_id, winner AS winner_id,
    (SELECT players.name AS winner_name
      FROM matches INNER JOIN players ON matches.winner = players.id),
    loser AS loser_id,
    (SELECT players.name AS loser_name
      FROM matches INNER JOIN players ON matches.loser = players.id),
    draw_flag FROM matches;

-- Match view that shows non-drawn matches
CREATE VIEW view_matches_no_draw AS
  SELECT match_id, winner_id, winner_name, loser_id, loser_name
    FROM view_matches_all WHERE draw_flag = FALSE;

-- Match view that shows drawn matches
CREATE VIEW view_matches_drawn AS
  SELECT match_id, winner_id AS player1_id, winner_name AS player1,
    loser_id AS player2_id, loser_name AS player2
    FROM view_matches_all WHERE draw_flag = TRUE;

-- Player view that shows his/her won matches
CREATE VIEW view_player_win_record AS
  SELECT players.id AS player_id, name, matches.id AS match_id
    FROM players INNER JOIN matches ON players.id = matches.winner
  WHERE draw_flag = FALSE;

-- Player view that shows his/her loss matches
CREATE VIEW view_player_loss_record AS
  SELECT players.id AS player_id, name, matches.id AS match_id
    FROM players INNER JOIN matches ON players.id = matches.loser
  WHERE draw_flag = FALSE;

-- Player view that shows his/her drawn matches
CREATE VIEW view_player_draw_record AS
  SELECT players.id AS player_id, name, matches.id AS match_id
    FROM players INNER JOIN matches ON players.id = matches.winner
    WHERE draw_flag = TRUE
  UNION
  SELECT players.id AS player_id, name, matches.id AS match_id
    FROM players INNER JOIN matches ON players.id = matches.loser
    WHERE draw_flag = TRUE;

-- Player view that shows all his/her matches
CREATE VIEW view_player_record AS
  SELECT * FROM view_player_win_record
  UNION
  SELECT * FROM view_player_loss_record
  UNION
  SELECT * FROM view_player_draw_record;
