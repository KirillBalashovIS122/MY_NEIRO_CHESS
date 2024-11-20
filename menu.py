import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.modes = ["1. Player vs Player", "2. Player vs AI", "3. AI vs AI"]

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        text = self.font.render("Choose game mode:", True, (0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 100))

        for i, mode in enumerate(self.modes):
            text = self.font.render(mode, True, (0, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "PvP"
                    elif event.key == pygame.K_2:
                        return "PvAI"
                    elif event.key == pygame.K_3:
                        return "AIvAI"
        return None
