Tournament Planner Project
=============

This project is

## How to run this Project

1. Download and install [Python ~2](https://www.python.org/downloads/)
1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
1. Download and install [Vagrant](https://www.vagrantup.com/)
1. From the folder `vagrant` of this repository, run the command `vagrant up`. Please allow time for vagrant to download dependencies and set up the virtual environment
1. Once vagrant complete, run `vagrant ssh` to remotely connect to the virtual machine
1. Navigate to `/vagrant/tournament` on the virtual machine
1. Run `psql` to enter `PostgreSQL CLI Interface`
1. Create tournament database with `CREATE DATABASE tournament`
1. Connect to the database with `\c tournament`
1. Create tables and views with `\i tournament.sql`
1. Run `\q` to exit the CLI
1. Run `python tounament_test.py`
