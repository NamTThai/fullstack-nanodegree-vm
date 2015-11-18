Pokemon Catalog Project
=============

If you are reading this document, that means you have made it to 12 years of life. Congratulation on surviving [BDBD](https://www.youtube.com/watch?v=1YRvXpLOft8) as well as various other infant mortality causes. It's time for you to start your wondrous adventure into [tall bushes](https://www.youtube.com/watch?v=q9zxbQSz-08) and meet some wonderful partners in crime. Scientists have encountered hundreds of Pokemon, in various shapes and sizes. `I'm tempted to say something about undocumented ones here`. Are you ready? We have a Pokedex giveaway!

## Pokedex starting kit

1. Once vagrant complete, run `vagrant ssh` to remotely connect to the virtual machine
1. Navigate to `/vagrant/catalog` on the virtual machine
1. `bower install`
1. Run `python db_setup.py`
1. Run `python app.py` to launch Pokedex local server
1. Browse `localhost:5000` to access your Pokedex

## Features
1. Your awesome gadget comes with 51 commonly found Pokemons!
1. View Pokemon entries, including their name, captured picture, typing and description
1. Document new Pokemon entry whenever you encounter one in the wild
1. Modify and delete entry that you have created
1. If you encounter a new Pokemon that might be of undiscovered Type, don't hesitate to contact us! We'll verify whether he/she is indeed of new Type and update Type list for you. (a.k.a if this is not obvious enough, don't add new Type on your own; you will break stuff)
1. Browse `localhost:5000/rss` to access a RSS feed of latest Pokedex entries.
1. Added security measure to prevent CSRF
