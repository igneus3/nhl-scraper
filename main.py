from db import NhlRepository
from game import process_game
                  
def main():
    gameProcessed = True
    gameId = 2023020001

    with NhlRepository() as repo:
        while gameProcessed:
            print(f'Started processing game: {gameId}')
            gameProcessed = process_game(repo, gameId)
            print(f'Finished processing game: {gameId}')
            gameId += 1

    print('\n\nFinished processing all played games')

if __name__ == '__main__':
    main()
