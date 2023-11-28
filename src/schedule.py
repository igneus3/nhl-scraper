from datetime import date, timedelta
import os
import pickle
import requests

from util import http_request_with_retry

def get_latest_game(repo):
    result = repo.get_latest_game(); 
    if result == None:
        result = {
            'gameDate' : '2003-09-01'
        }

    return result

def download_schedule(current_date):
    url = f'https://api-web.nhle.com/v1/schedule/{current_date}'
    return http_request_with_retry(url)

def get_schedule(current_date):
    path = f'data/schedules/{current_date}.pkl'
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    schedule = download_schedule(current_date)
    with open(path, 'wb') as file:
        pickle.dump(schedule, file)

    return schedule

def setup_folder(season):
    path = f'data/games/{season}'
    if os.path.isdir(path):
        return

    os.makedirs(path)

def process_schedule(repo, schedule):
    result = 0
    for day_of_week in range(7):
        day = schedule['gameWeek'][day_of_week]
        if len(day['games']) == 0:
            continue

        for game in day['games']:
            game_id = game['id']
            game_exists = repo.get_game(game_id) != None

            if game_exists:
                continue

            repo.insert_game(game_id, game['season'],  day['date'], False)
            result += 1

            setup_folder(game['season'])

    return result

def load_scheduled_games(repo):
    latest_game = get_latest_game(repo)

    delta = timedelta(days=7)
    next_season = date.fromisoformat(f'{date.today().year + 1}-09-01')
    current_date = date.fromisoformat(latest_game['gameDate'])

    while current_date < next_season:
        schedule = get_schedule(current_date)

        if schedule is None:
            current_date += delta
            continue

        added_games = process_schedule(repo, schedule)

        print('Week of {0} => Added {1} games'.format(current_date, added_games))

        if 'nextStartDate' not in schedule:
            print('Finished processing all scheduled games!')
            return

        current_date = date.fromisoformat(schedule['nextStartDate'])
