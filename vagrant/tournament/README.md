Tournament Planner Project
=============

This project provides functionalities to plan a [Swiss system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament)

## How to run this Project

1. Once vagrant complete, run `vagrant ssh` to remotely connect to the virtual machine
1. Navigate to `/vagrant/tournament` on the virtual machine
1. Run `psql` to enter `PostgreSQL CLI Interface`
1. Create tournament database with `CREATE DATABASE tournament`
1. Connect to the database with `\c tournament`
1. Create tables and views with `\i tournament.sql`
1. Run `\q` to exit the CLI
1. All the commands to successfully run and plan a tournament is located in `tournament.py`
1. To verify that all functions run correctly, run `python tounament_test.py`

## Basic Features
1. Store player information (full name) in database, subjecting to deletion and modification
1. Store match information (participants, outcome) in database, subjecting to deletion and modification
1. Retrieve player standings
1. Generate pairings for each round

## Extra Features
1. Draw is possible
1. If there are odd number of players, one player will have automatic win each round (walkover). No two players' number of walkovers can be different by 2.
1. There is no rematch between two players until both players have played against all other players
1. When two players have the same number of wins, they are ranked according to OMW (Opponent Match Wins), the total number of wins by players they have played against
