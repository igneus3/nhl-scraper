from argparse import ArgumentParser
from datetime import date
import logging
import os
import sqlite3
import traceback

from db import NhlRepository
from game import process_games
from schedule import load_scheduled_games

def register_adapters_converter():
    def adapt_date_iso(val):
        return val.isoformat()

    def convert_date(val):
        return date.fromisoformat(val.decode())

    sqlite3.register_adapter(date, adapt_date_iso)
    sqlite3.register_converter('date', convert_date)

def setup_data_folder():
    if not os.path.isdir('data'):
        os.makedirs('data')
        os.makedirs('data/schedules')
        os.makedirs('data/games')

def setup_logging(silent):
    log_level = logging.ERROR if silent else logging.INFO

    logging.basicConfig(level=log_level, format='[%(levelname)s]\t%(asctime)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
def main():
    parser = ArgumentParser('main_parser')
    parser.add_argument('--path', default='db/nhl.db', help='Set the path for the database file.')
    parser.add_argument('--silent', action='store_true', help='Set logging level to error.')
    args = parser.parse_args()

    register_adapters_converter()
    setup_data_folder()
    setup_logging(args.silent)

    with NhlRepository(args.path) as repo:
        load_scheduled_games(repo)

        process_games(repo) 

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f'{type(e).__name__}\t{e}')
        logging.error(traceback.format_exc())
