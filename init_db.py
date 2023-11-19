from argparse import ArgumentParser
from pathlib import Path
import sqlite3

def delete_db():
    db_path = Path('nhl.db')
    db_path.unlink(missing_ok=True)

def initialize_db():
    games_table = """
    CREATE TABLE IF NOT EXISTS games(
        id INTEGER PRIMARY KEY,
        processed INTEGER NOT NULL
    )
    """

    players_table = """
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY
    )
    """

    plays_table = """
    CREATE TABLE IF NOT EXISTS plays(
        game_id INTEGER REFERENCES games(id),
        event_id INTEGER NOT NULL,
        period INTEGER NOT NULL,
        period_type TEXT NOT NULL,
        time_in_period TEXT NOT NULL,
        time_remaining TEXT NOT NULL,
        home_team_defending_side TEXT NOT NULL,
        type_code INTEGER NOT NULL,
        type_desc_key TEXT NOT NULL,
        details TEXT,

        PRIMARY KEY (game_id, event_id)
    )
    """

    player_games_table = """
    CREATE TABLE IF NOT EXISTS player_games(
        game_id INTEGER REFERENCES games(id),
        player_id INTEGER REFERENCES players(id),
        assists INTEGER DEFAULT 0,
        blocked_shots INTEGER DEFAULT 0,
        faceoff_wins INTEGER DEFAULT 0,
        faceoffs INTEGER DEFAULT 0,
        giveaways INTEGER DEFAULT 0,
        goals INTEGER DEFAULT 0,
        hits_given INTEGER DEFAULT 0,
        hits_received INTEGER DEFAULT 0,
        missed_shots INTEGER DEFAULT 0,
        penalties_committed INTEGER DEFAULT 0,
        penalties_drawn INTEGER DEFAULT 0,
        penalties_served INTEGER DEFAULT 0,
        primary_assists INTEGER DEFAULT 0,
        saves INTEGER DEFAULT 0,
        secondary_assists INTEGER DEFAULT 0,
        shots INTEGER DEFAULT 0,
        shots_on_goal INTEGER DEFAULT 0,
        so_failed_shot INTEGER DEFAULT 0,
        so_shots INTEGER DEFAULT 0,
        takeaways INTEGER DEFAULT 0,

        PRIMARY KEY (game_id, player_id)
    )
    """

    tables = [games_table, players_table, plays_table, player_games_table]

    con = sqlite3.connect('nhl.db')
    cur = con.cursor()

    for table in tables:
        cur.execute(table)

    con.close()

def main():
    parser = ArgumentParser('init_db_parser')
    parser.add_argument('--empty', action='store_true', help='Setting this flag will erase all data!')
    args = parser.parse_args()

    if args.empty:
        delete_db()

    initialize_db()

if __name__ == '__main__':
    main()

