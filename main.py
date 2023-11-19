from datetime import date, timedelta
import requests
import sqlite3

from db import NhlRepository
from game import process_game

def register_adapters_converter():
    def adapt_date_iso(val):
        return val.isoformat()

    def convert_date(val):
        return date.fromisoformat(val.decode())

    sqlite3.register_adapter(date, adapt_date_iso)
    sqlite3.register_converter('date', convert_date)
        
def load_scheduled_games(repo):
    # TODO: Process schedule to find games for the season
    latest_game = repo.get_latest_game(); 
    if latest_game == None:
        latest_game = {
            'gameDate' : '1980-09-01'
        }

    next_season = date.fromisoformat(f'{date.today().year + 1}-09-01')

    # TODO: Load games into database
    current_date = date.fromisoformat(latest_game['gameDate'])
    count = 0
    delta = timedelta(days=7)
    while current_date < next_season:
        # /v1/schedule/2023-11-17 or /v1/schedule/now
        result = None
        url = f'https://api-web.nhle.com/v1/schedule/{current_date}'

        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
        elif response.status_code == 404:
            current_date += delta
            continue

        added_games = 0
        for day_of_week in range(7):
            day = result['gameWeek'][day_of_week]
            if len(day['games']) == 0:
                continue

            for game in day['games']:
                game_id = game['id']
                game_exists = repo.get_game(game_id) != None

                if game_exists:
                    continue

                repo.insert_game(game_id, day['date'], False)
                added_games += 1


        print('Week of {0} => Added {1} games'.format(result['nextStartDate'], added_games))
        current_date = date.fromisoformat(result['nextStartDate'])


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
