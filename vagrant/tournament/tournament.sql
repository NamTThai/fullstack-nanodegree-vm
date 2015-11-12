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

-- Player view that shows his/her number of walkovers
CREATE VIEW view_player_walkover AS
  SELECT id, name,
    (SELECT COUNT(*) FROM matches
      WHERE matches.loser IS NULL and players.id = matches.winner
    ) AS number_of_walkover
    FROM players;

-- Player view that shows his/her number of non-walkovers
CREATE VIEW view_player_non_walkover AS
  SELECT id, name,
    (SELECT COUNT(*) FROM matches
      WHERE matches.loser IS NOT NULL AND
        (players.id = matches.winner OR players.id = matches.loser)
    ) AS number_of_non_walkover
    FROM players;

-- Player view that show his/her possible matchup. This allows for battling againts oneself
CREATE VIEW view_player_possible_matchup AS
  SELECT A.id, A.name, B.id AS opponent FROM players AS A CROSS JOIN players AS B;

-- Player view that show his/her opponents and number of times they match up and
-- his/her opponent's omw (opponent match wins)
CREATE VIEW view_player_versus AS
  SELECT id, name, opponent,
    (SELECT COUNT(*) FROM matches
      WHERE (matches.winner = matchup.id AND matches.loser = matchup.opponent) OR
      (matches.winner = matchup.opponent AND matches.loser = matchup.id)
    ) AS number_of_matchup,
    (SELECT COUNT(*) FROM view_player_win_record AS win
      WHERE matchup.opponent = win.player_id) AS omw
    FROM view_player_possible_matchup AS matchup
    WHERE id != opponent;

-- Player view that shows his/her number of won, omw (opponent match wins),
-- non-walkover matches and total matches
CREATE VIEW view_player_standing AS
  SELECT id, name,
    (SELECT COUNT(*) FROM view_player_win_record AS win
      WHERE players.id = win.player_id) AS number_of_win,
    (SELECT SUM(omw) FROM view_player_versus AS versus
      WHERE players.id = versus.id) AS omw,
    (SELECT number_of_non_walkover FROM view_player_non_walkover AS walkover
      WHERE walkover.id = players.id) AS number_of_non_walkover,
    (SELECT COUNT(*) FROM view_player_record AS total
      WHERE total.player_id = players.id) AS number_of_matches
    FROM players;
