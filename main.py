from datetime import date
import requests
import sqlite3

from db import NhlRepository
from game import process_game
from schedule import load_scheduled_games

def register_adapters_converter():
    def adapt_date_iso(val):
        return val.isoformat()

    def convert_date(val):
        return date.fromisoformat(val.decode())

    sqlite3.register_adapter(date, adapt_date_iso)
    sqlite3.register_converter('date', convert_date)
        
# TODO: Remane this
def games(repo):
    game_processed = True
    game_id = 2023020250

    while game_processed:
        game = repo.get_game(game_id)

        if game is not None and game['processed']:
            print(f'Skipping {game_id} as it has already been processed.')
        else:
            print(f'Started processing game: {game_id}')
            game_processed = process_game(repo, game_id)
            print(f'Finished processing game: {game_id}')

        game_id += 1

    print('\n\nFinished processing all played games')
                  
def main():
    register_adapters_converter()

    with NhlRepository() as repo:
        load_scheduled_games(repo)
         # TODO: Query DB for games that have not been processed in asc order by game ID
         # games(repo) 

         # TODO: Check if game has been played via nhle api

         # TODO: If game has been played, process database

         # TODO: Abort if no newly played games


if __name__ == '__main__':
    main()
