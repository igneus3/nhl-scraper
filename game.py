import requests

from player import Player
from play import process_play_with_logging

def get_game_data(game_id):
    result = None
    url = f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'

    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()

    return result

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

    if data['gameState'] == 'FUT':
        print('Game no played yet!')
        return False

    play_data = get_play_data(data)
    save_play_data(repo, game_id, play_data)

    players = get_players(data)
    player_data = build_player_data(play_data, players)
    save_player_data(repo, game_id, player_data)

    return True
