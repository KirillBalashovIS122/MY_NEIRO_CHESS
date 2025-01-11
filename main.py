import pygame
from menu import Menu
from game import Game
from chess_ai import ChessAI

pygame.init()

WIDTH, HEIGHT = 600, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

def show_loading_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Training AI...", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    # Прогресс-бар
    progress_bar_width = 400
    progress_bar_height = 20
    progress_bar_rect = pygame.Rect((WIDTH - progress_bar_width) // 2, HEIGHT // 2, progress_bar_width, progress_bar_height)
    pygame.draw.rect(screen, (0, 0, 0), progress_bar_rect, 2)

    pygame.display.flip()
    return progress_bar_rect

def update_progress_bar(screen, progress_bar_rect, progress):
    pygame.draw.rect(screen, (0, 255, 0), (progress_bar_rect.x, progress_bar_rect.y, progress * progress_bar_rect.width, progress_bar_rect.height))
    pygame.display.flip()

def main():
    running = True
    menu = Menu(screen)
    game = Game(screen)
    chess_ai = ChessAI()

    while running:
        game_mode = menu.run()
        if game_mode:
            if game_mode in ["PvAI", "AIvAI"]:
                # Показываем экран загрузки
                progress_bar_rect = show_loading_screen(screen)

                # Запускаем обучение нейронной сети
                for epoch in range(10):  # Пример: 10 эпох обучения
                    chess_ai.train(data, labels, epochs=1)  # Обучаем на 1 эпоху
                    progress = (epoch + 1) / 10  # Прогресс от 0 до 1
                    update_progress_bar(screen, progress_bar_rect, progress)

            print(f"Starting game mode: {game_mode}")
            game.run(game_mode, chess_ai)
            print("Game finished")
        else:
            running = False

    print("Exiting program")
    pygame.quit()

if __name__ == '__main__':
    main()
