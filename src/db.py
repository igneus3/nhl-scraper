import json
import sqlite3

from player import Player

class NhlRepository:
    def __init__(self, path):
        self.__connection = sqlite3.connect(path)
        self.__connection.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.__connection.close()
    
    def __execute(self, statement, params=()):
        cursor = self.__connection.cursor()

        cursor.execute(statement, params)
        self.__connection.commit()

        cursor.close()

    def __find_one(self, query):
        cursor = self.__connection.cursor()

        records = cursor.execute(query) 
        result = records.fetchone()

        cursor.close()

        return result

    def __find_many(self, query):
        cursor = self.__connection.cursor()

        records = cursor.execute(query)
        result = records.fetchmany()

        cursor.close()

        return result

    def insert_game(self, game_id, gameDate, processed):
        statement = """
        INSERT INTO games(id, gameDate, processed) VALUES (?, ?, ?)
        """
        params = (game_id, gameDate, processed)

        self.__execute(statement, params)

    def get_game(self, game_id):
        query = 'SELECT id, processed  FROM GAMES WHERE id = {0}'.format(game_id)

        return self.__find_one(query)

    def get_latest_game(self, only_unprocessed=False):
        query = 'SELECT id, processed, gameDate FROM games ORDER BY gameDate DESC'

        return self.__find_one(query)

    def get_unprocessed_games(self, limit = 100):
        query = 'SELECT id, gameDate FROM games WHERE processed = FALSE ORDER BY gameDate ASC LIMIT {0}'.format(limit)

        result = self.__find_many(query)

        return None if result == [] else result

    def mark_game_processed(self, game_id):
        query = "UPDATE games SET processed = TRUE WHERE id = '{0}'".format(game_id)

        return self.__execute(query)

    def insert_player_game(self, game_id, player):
        statement = """
        INSERT INTO player_games
        (
            game_id,
            player_id,
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
            saves,
            secondary_assists,
            shots,
            shots_on_goal,
            so_failed_shot,
            so_shots,
            takeaways
        ) VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?
        )
        """
        params = (
            game_id, player.player_id, player.assists, player.blocked_shots,
            player.faceoff_wins, player.faceoffs, player.giveaways, player.goals,
            player.hits_given, player.hits_received, player.missed_shots, player.penalties_committed,
            player.penalties_drawn, player.penalties_served, player.primary_assists, player.saves,
            player.secondary_assists, player.shots, player.shots_on_goal, player.so_failed_shot,
            player.so_shots, player.takeaways
        )

        self.__execute(statement, params)

    def insert_play(self, game_id, play):
        statement = """
        INSERT INTO plays
        (
            game_id,
            event_id,
            period,
            period_type,
            time_in_period,
            time_remaining,
            type_code,
            type_desc_key,
            details
        )
        VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?
        )
        """
        params = (
           game_id, play['eventId'], play['period'], play['periodDescriptor']['periodType'],
           play['timeInPeriod'], play['timeRemaining'], play['typeCode'],
           play['typeDescKey']
        )

        if 'details' in play:
            params += (json.dumps(play['details']),)
        else:
            params += (None,)

        self.__execute(statement, params)



if __name__ == '__main__':
    player = Player(1)

    player.assists = 1
    player.blocked_shots = 2
    player.faceoff_wins = 3
    player.faceoffs = 4
    player.giveaways = 5
    player.goals = 6
    player.hits_given = 7
    player.hits_received = 8
    player.missed_shots = 9
    player.penalties_committed = 10
    player.penalties_drawn = 11
    player.penalties_served = 12
    player.primary_assists = 13
    player.saves = 14
    player.secondary_assists = 15
    player.shots = 16
    player.shots_on_goal = 17
    player.so_failed_shot = 18
    player.so_shots = 19
    player.takeaways = 20

    with NhlRepository() as repo:
        repo.insert_player_game(2023020001, player)
