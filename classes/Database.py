import sqlite3

class DataBaseR6:
    def __init__(self):
        self.conn = sqlite3.connect("r6_players.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS R6_players 
        (discord_id INT PRIMARY KEY,
        nickname TEXT, 
        kills INT, 
        deaths INT, 
        wins INT,
        loses INT,
        mmr INT
        );""")

    def add_players(self, player):
        player_data = (player.member_id, player.nickname, player.kills, player.deaths, player.wins, player.loses,
                       player.mmr)
        self.cursor.execute("INSERT INTO R6_players VALUES (?,?,?,?,?,?,?);", player_data)
        self.conn.commit()