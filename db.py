import sqlite3

from player import Player

class NhlRepository:
    def __init__(self):
        self.connection = sqlite3.connect('nhl.db')

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.connection.close()

    def insert_player_game(self, gameId, player):
        insert_statement = """
        INSERT INTO player_games
        (
            gameId,
            playerId,
            assists,
            blocked_shots,
            faceoff_wins,
            faceoffs,
            giveaways,
            goals,
            hits_given,
            hits_received,
            missed_shots,
            penalties_committed,
            penalties_drawn,
            penalties_served,
            primary_assists,
            secondary_assists,
            shots,
            shots_on_goal,
            so_failed_shot,
            so_shots,
            takeaways
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            gameId, player.playerId,
            player.assists, player.blocked_shots, player.faceoff_wins, player.faceoffs,
            player.giveaways, player.goals, player.hits_given, player.hits_received,
            player.missed_shots, player.penalties_committed, player.penalties_drawn, player.penalties_served,
            player.primary_assists, player.secondary_assists, player.shots, player.shots_on_goal,
            player.so_failed_shot, player.so_shots, player.takeaways
        )

        cursor = self.connection.cursor()

        cursor.execute(insert_statement, params)
        self.connection.commit()

        cursor.close()

