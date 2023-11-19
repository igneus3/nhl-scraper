from enum import EnumMeta, StrEnum
import requests

from player import Player
from play import process_play_with_logging
from util import http_request

class GameStateMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

class GameState(StrEnum, metaclass=GameStateMeta):
        FINISHED = 'FINAL'
        FUTURE = 'FUT'
        LIVE = 'LIVE'
        PLAYED  = 'OFF'

def get_game_data(game_id):
    url = f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'
    return http_request(url)

def get_play_data(data):
    return data['plays']

def save_play_data(repo, game_id, plays):
    for play in plays:
        repo.insert_play(game_id, play)

def get_players(data):
    return data['rosterSpots']

def build_player_data(plays, players):
    player_data = dict()

    for player in players:
        player_id = player['playerId']
        if player_id in player_data:
           continue 

        player_data[player_id] = Player(player_id)

    for play in plays:
        process_play_with_logging(play, player_data)

    return player_data

def save_player_data(repo, game_id, players):
    for _, player in players.items():
        repo.insert_player_game(game_id, player)

def process_game(repo, game_id):
    data = get_game_data(game_id)
        
    if data is None:
        print("Game not found!")
        return False

    game_state = data['gameState']
    if game_state not in list(GameState):
        print('Unseen game state: {0}\nGame not processed!'.format(game_state))
        return False

    game_played = game_state == 'OFF'
    repo.insert_game(game_id, game_played)

    if not game_played:
        return True

    play_data = get_play_data(data)
    save_play_data(repo, game_id, play_data)

    players = get_players(data)
    player_data = build_player_data(play_data, players)
    save_player_data(repo, game_id, player_data)

    return True
