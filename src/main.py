from argparse import ArgumentParser
from datetime import date
import sqlite3

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
        
# TODO: Remane this
                  
def main():
    parser = ArgumentParser('main_parser')
    parser.add_argument('--path', default='db/nhl.db', help='Set the path for the database file.')
    args = parser.parse_args()

    register_adapters_converter()

    with NhlRepository(args.path) as repo:
        load_scheduled_games(repo)

        #process_games(repo) 

if __name__ == '__main__':
    main()
