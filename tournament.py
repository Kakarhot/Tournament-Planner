#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    cursor = conn.cursor()
    return conn, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("TRUNCATE match")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("TRUNCATE player CASCADE")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("SELECT count(*) FROM player")
    count = c.fetchall()[0][0]
    conn.close

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()

    query = "INSERT INTO player (name) VALUES (%s)"
    param = (name,)
    c.execute(query, param)

    query = "SELECT id FROM player WHERE name = (%s)"
    param = (name,)
    c.execute(query, param)
    player_id = c.fetchall()[0][0]

    query = "INSERT INTO match (id, num_of_matches, num_of_wins) VALUES (" + str(player_id) + ", 0, 0)"
    c.execute(query)   # Insert the player into the match table with same id.
    conn.commit()
    conn.close()




def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []

    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    query = "SELECT COALESCE(max(num_of_wins),0) FROM player_match"
    c.execute(query)   # Get the maximum number of wins, set it to 0 if it's NULL.
    max_win = c.fetchall()[0][0]

    for wins in range(max_win, -1, -1):
        query = "SELECT id, name, COALESCE(num_of_wins,0), COALESCE(num_of_matches,0) FROM player_match WHERE COALESCE(player_match.num_of_wins,0) = " + str(wins)
        c.execute(query)   # Get data from the VIEW. Set the value to 0 if it's NULL.
        standings += c.fetchall()
    
    conn.close()

    return standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor() 

    query = "SELECT num_of_wins FROM match WHERE id = " + str(winner)
    c.execute(query)
    num_of_wins_winner = c.fetchall()[0][0] + 1

    query = "SELECT num_of_matches FROM match WHERE id = " + str(winner)
    c.execute(query)
    num_of_matches_winner = c.fetchall()[0][0] + 1 

    query = "SELECT num_of_matches FROM match WHERE id = " + str(loser)
    c.execute(query)
    num_of_matches_loser = c.fetchall()[0][0] + 1   

    query = "UPDATE match SET num_of_wins = " + str(num_of_wins_winner) + " WHERE id = " + str(winner)
    c.execute(query)   # Update num_of_wins for the winner.

    query = "UPDATE match SET num_of_matches = " + str(num_of_matches_winner) + " WHERE id = " + str(winner)
    c.execute(query)   # Update num_of_matches for both the winner and loser.

    query = "UPDATE match SET num_of_matches = " + str(num_of_matches_loser) + " WHERE id = " + str(loser)
    c.execute(query)
    
    conn.commit()
    conn.close()



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairing = []

    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("SELECT max(num_of_wins) FROM match")
    max_win = c.fetchall()[0][0]

    for wins in range(0,max_win + 1):   # loop through num_of_wins
        query = "SELECT player.id, player.name FROM player, match WHERE player.id = match.id and num_of_wins = " + str(wins)
        c.execute(query)
        res = c.fetchall()
        
        pairs= []
        flag = 0
        for e in res:
            if flag == 0:   # it's the first element in the tuple
                pairs = e
                flag = 1
            else:   # it's the second element in the tuple
                pairs += e   
                flag = 0
                pairing.append(tuple(pairs))

    conn.close()
    
    return pairing
