from db import NhlRepository
from game import process_game
                  
def main():
    game_processed = True
    game_id = 2023020001

    with NhlRepository() as repo:
        while game_processed:
            print(f'Started processing game: {game_id}')
            game_processed = process_game(repo, game_id)
            print(f'Finished processing game: {game_id}')
            game_id += 1

    print('\n\nFinished processing all played games')

if __name__ == '__main__':
    main()
