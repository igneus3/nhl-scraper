from datetime import date
from enum import EnumMeta, StrEnum
from logging import info, warn
import os
import pickle
import requests

from game_parser import GameParser
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
    return http_request_with_retry(url)

def get_game_data(game_id, season):
    path = f'data/games/{season}/{game_id}.html'
    if os.path.isfile(path):
        with open(path, mode='r', encoding='utf-8') as file:
            file_game = file.read()
            if file_game == '':
                return None
            else:
                return file_game

    dl_game = download_game_data(game_id, season)
    with open(path, mode='w', encoding='utf-8') as file:
        if dl_game is None:
            file.write('')
        else:
            file.write(dl_game)

    return dl_game

def save_play_data(repo, game_id, plays):
    for play in plays:
        try:
            repo.insert_play(game_id, play)
        except Exception as e:
            e.add_note(f'{game_id} => {play}')
            raise e

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
        warn(f'Game {game_id} not found!')
        return True

    game_parser = GameParser(data, game_id)

    game_state = game_parser.get_game_state()

    if game_state is None:
        warn(f'{game_id}\tGame file was invalid.')
        return True

    if game_state not in list(GameState):
        info('Unseen game state: {0}\nGame not processed!'.format(game_state))
        return False

    game_played = game_state == GameState.PLAYED or game_state == GameState.FINISHED
    if not game_played:
        return True

    play_data = game_parser.get_play_data()
    save_play_data(repo, game_id, play_data)

    #players = get_players(data)
    #player_data = build_player_data(play_data, players)
    #save_player_data(repo, game_id, player_data)

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
