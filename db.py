import json
import sqlite3

from player import Player

class NhlRepository:
    def __init__(self):
        self.connection = sqlite3.connect('nhl.db')
        self.connection.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.connection.close()

    def __insert(self, statement, params):
        cursor = self.connection.cursor()

        cursor.execute(statement, params)
        self.connection.commit()

        cursor.close()

    def __find_one(self, query):
        cursor = self.connection.cursor()

        records = cursor.execute(query) 
        result = records.fetchone()

        cursor.close()

        return result

    def insert_game(self, game_id, played):
        statement = """
        INSERT INTO games(id, processed) VALUES (?, ?)
        """
        params = (game_id, played)

        self.__insert(statement, params)

    def get_game(self, game_id):
        query = 'SELECT id, processed  FROM GAMES WHERE id = {0}'.format(game_id)

        return self.__find_one(query)


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

        self.__insert(statement, params)

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
            home_team_defending_side,
            type_code,
            type_desc_key,
            details
        )
        VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?
        )
        """
        params = (
           game_id, play['eventId'], play['period'], play['periodDescriptor']['periodType'],
           play['timeInPeriod'], play['timeRemaining'], play['homeTeamDefendingSide'], play['typeCode'],
           play['typeDescKey']
        )

        if 'details' in play:
            params += (json.dumps(play['details']),)
        else:
            params += (None,)

        self.__insert(statement, params)



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
