#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def checkForRematch(p1, p2):
    """Check whether two players can match up

    Condition for matching up: either two players have never played before, or
    they have played with all other players at least the same number of times

    Args:
        p1:  player 1 ID
        p2:  player 2 ID

    Return: whether they can be paired against each others
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select number_of_matchup, (select min(number_of_matchup) from view_player_versus where id = %(p1)s) as min from view_player_versus where id = %(p1)s and opponent = %(p2)s", {"p1": p1, "p2": p2})
    row = cursor.fetchone()
    connection.close()
    if row[0] > row[1]:
        return False
    else:
        return True


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from matches")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from players")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select count(*) from players")
    row = cursor.fetchone()
    connection.close()
    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("insert into players (name) values (%(name)s)",
                   {"name": name})
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Tie breaks are determined by OMW (opponent match wins) and then number of
    non-walkover matches.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select id, name, number_of_win, number_of_matches from " +
                   "view_player_standing order by number_of_win desc, omw "
                   "desc, number_of_non_walkover desc")
    rows = cursor.fetchall()
    connection.close()
    return rows


def reportMatch(winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw:  whether the match is a draw
    """
    connection = connect()
    cursor = connection.cursor()
    if (loser is None):
        cursor.execute("insert into matches (winner, draw_flag) values " +
                       "(%(winner)s, %(draw)s)",
                       {"winner": winner, "draw": draw})
    else:
        cursor.execute("insert into matches (winner, loser, draw_flag) values" +
                       " (%(winner)s, %(loser)s, %(draw)s)",
                       {"winner": winner, "loser": loser, "draw": draw})
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings, prioritizing on matches that haven't
    happened

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select id, name from view_player_standing order by number_of_win")
    playerList = cursor.fetchall()
    swissPairingsCheckForWalkover(playerList)
    pairings = []
    # Ensure that there is no rematch until necessary
    while len(playerList) > 0:
        p1 = playerList[0]
        # Iterate over the rest of playerList to find an eligible match up
        for i in xrange(1, len(playerList)):
            p2 = playerList[i]
            if (checkForRematch(p1[0], p2[0])):
                pairings.append(p1 + p2)
                playerList.remove(p1)
                playerList.remove(p2)
                break
    connection.close()
    return pairings


def swissPairingsCheckForWalkover(playerList):
    """Assign one player automatic win if there are odd number of players

    No two players' number of automatic wins are greater than 2. After assigning
    a player walkover, remove that player from playerList

    Args:
        playerList:  list of player in each round, has to be odd
    """
    if (len(playerList) % 2 == 0):
        return
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select id from view_player_walkover" +
                   " order by number_of_walkover limit 1")
    row = cursor.fetchone()
    playerId = row[0]
    connection.close()
    reportMatch(playerId, None, False)
    for player in playerList:
        if player[0] == playerId:
            playerList.remove(player)
            break
    return
