from datetime import date
from enum import EnumMeta, StrEnum
from logging import info, warn
import os
import pickle
import requests

from player import Player
from play import process_play_with_logging
from util import http_request_with_retry

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

def download_game_data(game_id, season):
    url = f'https://www.nhl.com/scores/htmlreports/{season}/PL{str(game_id)[4:]}.HTM'
    #url = f'https://www.nhl.com/scores/htmlreports/20072008/PL020001.HTM'
    return http_request_with_retry(url)

def get_game_data(game_id, season):
    path = f'data/games/{season}/{game_id}.pkl'
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    dl_game = download_game_data(game_id, season)
    with open(path, 'wb') as file:
        pickle.dump(dl_game, file)

    return dl_game

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

def process_game(repo, game_id, season):
    data = get_game_data(game_id, season)
        
    if data is None:
        return False
        warn(f'Game {game_id} not found!')

    game_state = data['gameState']
    if game_state not in list(GameState):
        info('Unseen game state: {0}\nGame not processed!'.format(game_state))
        return False

    game_played = game_state == GameState.PLAYED or game_state == GameState.FINISHED
    if not game_played:
        return True

    play_data = get_play_data(data)
    save_play_data(repo, game_id, play_data)

    players = get_players(data)
    player_data = build_player_data(play_data, players)
    save_player_data(repo, game_id, player_data)

    return True

def process_games(repo):
    today = date.today()

    processed_a_game = False
    has_played_games = True
    while(has_played_games):
        games = repo.get_unprocessed_games()

        if games is None:
            has_played_games = False
            break;

        for game in games:
            if date.fromisoformat(game['gameDate']) >= today:
                has_played_games = False
                break

            game_id = game['id']

            info(f'Started processing game: {game_id}')
            game_processed = process_game(repo, game_id, game['season'])
            if game_processed:
                processed_a_game = True
                repo.mark_game_processed(game_id)
                info(f'Finished processing game: {game_id}')
            else:
                warn(f'There was an issues processing game: {game_id}')

    if processed_a_game:
        info('\n\nFinished processing all played games')
    else:
        info('\n\nNo games needed processing')
