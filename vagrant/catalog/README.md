Pokemon Catalog Project
=============

If you are reading this document, that means you have made it to 12 years of life. Congratulation on surviving [BDBD](https://www.youtube.com/watch?v=1YRvXpLOft8) as well as various other infant mortality causes. It's time for you to start your wondrous adventure into [tall bushes](https://www.youtube.com/watch?v=q9zxbQSz-08) and meet some wonderful partners in crime. Scientists have encountered hundreds of Pokemon, in various shapes and sizes. `I'm tempted to say something about undocumented ones here`. Are you ready? We have a Pokedex giveaway!

## Pokedex starting kit

1. Once vagrant complete, run `vagrant ssh` to remotely connect to the virtual machine
1. Navigate to `/vagrant/catalog` on the virtual machine
1. `bower install`
1. Run `python db_setup.py`

## Basic Features
1. Your awesome gadget comes with 51 commonly found Pokemons!
1. Store player information (full name) in database, subjecting to deletion and modification
1. Store match information (participants, outcome) in database, subjecting to deletion and modification
1. Retrieve player standings
1. Generate pairings for each round

## Extra Features
1. Draw is possible
1. If there are odd number of players, one player will have automatic win each round (walkover). No two players' number of walkovers can be different by 2.
1. There is no rematch between two players until both players have played against all other players
1. When two players have the same number of wins, they are ranked according to OMW (Opponent Match Wins), the total number of wins by players they have played against
