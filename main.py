import pygame
from menu import Menu
from game import Game

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

def main():
    running = True
    menu = Menu(screen)
    game = Game(screen)

    while running:
        game_mode = menu.run()
        if game_mode:
            print(f"Starting game mode: {game_mode}")
            game.run(game_mode)
            print("Game finished")
        else:
            running = False

    print("Exiting program")
    pygame.quit()

if __name__ == '__main__':
    main()
