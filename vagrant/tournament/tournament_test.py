#!/usr/bin/env python
#
# Test cases for tournament.py

import tournament


def testDeleteMatches():
    tournament.deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    tournament.deleteMatches()
    tournament.deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    tournament.deleteMatches()
    tournament.deletePlayers()
    c = tournament.countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Chandra Nalaar")
    c = tournament.countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Markov Chaney")
    tournament.registerPlayer("Joe Malik")
    tournament.registerPlayer("Mao Tsu-hsi")
    tournament.registerPlayer("Atlanta Hope")
    c = tournament.countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    tournament.deletePlayers()
    c = tournament.countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Melpomene Murray")
    tournament.registerPlayer("Randy Schwartz")
    standings = tournament.playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Bruno Walton")
    tournament.registerPlayer("Boots O'Neal")
    tournament.registerPlayer("Cathy Burton")
    tournament.registerPlayer("Diane Grant")
    standings = tournament.playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    tournament.reportMatch(id1, id2, False)
    tournament.reportMatch(id3, id4, False)
    standings = tournament.playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Twilight Sparkle")
    tournament.registerPlayer("Fluttershy")
    tournament.registerPlayer("Applejack")
    tournament.registerPlayer("Pinkie Pie")
    standings = tournament.playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    tournament.reportMatch(id1, id2, False)
    tournament.reportMatch(id3, id4, False)
    pairings = tournament.swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testDrawMatch():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Ann")
    tournament.registerPlayer("Beth")
    standings = tournament.playerStandings()
    [id1, id2] = [row[0] for row in standings]
    tournament.reportMatch(id1, id2, True)
    standings = tournament.playerStandings()
    [(pid1, p1, pwin1, ptotal1), (pid2, p2, pwin2, ptotal2)] = standings
    correct_result = set([frozenset([0, 1]), frozenset([0, 1])])
    actual_result = set([frozenset([pwin1, ptotal1]), frozenset([pwin2, ptotal2])])
    if correct_result != actual_result:
        raise ValueError("Incorrect result after a drawn match")
    [player1_total, player2_total] = [row[3] for row in standings]

    print "9. After a drawn match, neither player get additional win"


def testWalkover():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Ann")
    tournament.registerPlayer("Beth")
    tournament.registerPlayer("Cathy")
    pairings = tournament.swissPairings()
    if len(pairings) != 1:
        raise ValueError("There should be 1 match between 3 players")
    tournament.reportMatch(pairings[0][0], pairings[0][2], False)
    standings = tournament.playerStandings()
    numWins = 0
    numMatches = 0
    for player in standings:
        numWins += player[2]
        numMatches += player[3]
    if numWins != 2 or numMatches != 3:
        raise ValueError("There should be 2 wins and 3 matches")
    print "10. For 3 players tournament, one player gets automatic win"


def testRematch():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Ann")
    tournament.registerPlayer("Beth")
    tournament.registerPlayer("Cathy")
    tournament.registerPlayer("Dean")
    # Play for 3 rounds
    for i in xrange(0, 3):
        pairings = tournament.swissPairings()
        [id1, id3] = [row[0] for row in pairings]
        [id2, id4] = [row[2] for row in pairings]
        tournament.reportMatch(id1, id2, False)
        tournament.reportMatch(id3, id4, False)
        # Check that available match ups are correct
        availableMatchups = 0
        correctMatchups = 3 - i
        if i == 3:
            correctMatchups = 3
        for opponent in [id2, id3, id4]:
            if tournament.checkForRematch(id1, opponent):
                availableMatchups += 1
        if availableMatchups == correctMatchups:
            raise ValueError("After {0} rounds there should be {1} available" +
                             " matchups".format(i + 1, availableMatchups))
    print("11. There is no rematch between players until each players have " +
          "played againts all other players")


def testOmw():
    tournament.deleteMatches()
    tournament.deletePlayers()
    tournament.registerPlayer("Ann")
    tournament.registerPlayer("Beth")
    tournament.registerPlayer("Cathy")
    pairings = tournament.swissPairings()
    tournament.reportMatch(pairings[0][0], pairings[0][2], False)
    standings = tournament.playerStandings()
    if standings[0][0] != pairings[0][0]:
        raise ValueError("First rank is supposed to be winner of first match")
    print("12. Tie breaks are settled by OMW")


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testDrawMatch()
    testWalkover()
    testRematch()
    testOmw()
    print "Success!  All tests pass!"
