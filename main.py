import pygame
from menu import Menu
from game import Game

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MY Chess Game')

def main():
    running = True
    menu = Menu(screen)
    game = Game(screen)

    while running:
        game_mode = menu.run()
        if game_mode:
            game.run(game_mode)
        else:
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()
