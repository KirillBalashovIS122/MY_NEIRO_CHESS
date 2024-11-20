import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.modes = [
            "1. Player vs Player",
            "2. Player vs AI",
            "3. AI vs AI",
            "4. Exit"
        ]
        self.buttons = []

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        text = self.font.render("Choose game mode:", True, (0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 100))

        self.buttons = []
        for i, mode in enumerate(self.modes):
            text = self.font.render(mode, True, (0, 0, 0))
            x = self.screen.get_width() // 2 - text.get_width() // 2
            y = 200 + i * 50
            self.buttons.append((pygame.Rect(x, y, text.get_width(), text.get_height()), mode))
            self.screen.blit(text, (x, y))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for rect, mode in self.buttons:
                        if rect.collidepoint(pos):
                            if mode == "Exit":
                                return None
                            elif mode.startswith("1"):
                                return "PvP"
                            elif mode.startswith("2"):
                                return "PvAI"
                            elif mode.startswith("3"):
                                return "AIvAI"
        return None
