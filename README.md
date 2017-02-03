# Tournament Planner

### Description:

The tournament planner is a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

### How to build:

1. First you need to be using the Linux system or a virtual machine with PostgreSQL installed.

2. In command line, get to the folder where you download the module.

3. Run psql followed by \i tournament.sql to build and access the database.

4. To run the series of tests, type \q then python tournament_test.py.
