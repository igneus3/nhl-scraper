import requests

from player import Player
from play import PlayNotFoundError, process_play_with_logging

def get_game_data(gameId):
    result = None
    url = f'https://api-web.nhle.com/v1/gamecenter/{gameId}/play-by-play'

    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()

    return result

def get_players(data):
    result = dict()
    players = data['rosterSpots']

    for player in players:
        player_id = player['playerId']
        if player_id in result:
           continue 

        result[player_id] = Player(player_id)

    return result

def process_plays(data, players):
    plays = data['plays']

    for play in plays:
        process_play_with_logging(play, players)

def save_players(repo, gameId, players):
    for _, player in players.items():
        repo.insert_player_game(gameId, player)

def process_game(repo, gameId):
    data = get_game_data(gameId)
        
    if data is None:
        print("Game not found!")
        return False

    players = get_players(data)
        
    process_plays(data, players)

    save_players(repo, gameId, players)

    if len(players) == 0:
        print('Game no played yet!')
        return False

    return True
