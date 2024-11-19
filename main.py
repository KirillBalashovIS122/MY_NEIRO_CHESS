import pygame
import os
import cairosvg
from PIL import Image
from io import BytesIO

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paths to assets
ASSETS_PATH = "D:/MY_NEIRO_CHESS/assets"
BOARD_PATH = os.path.join(ASSETS_PATH, "board")
PIECES_PATH = os.path.join(ASSETS_PATH, "pieces")

# Load assets
def load_svg(path):
    # Convert SVG to PNG using cairosvg
    png_data = cairosvg.svg2png(url=path, output_width=SQUARE_SIZE, output_height=SQUARE_SIZE)
    png_file = Image.open(BytesIO(png_data)).convert("RGBA")
    return pygame.image.fromstring(png_file.tobytes(), png_file.size, png_file.mode)

dark_square = load_svg(os.path.join(BOARD_PATH, "square brown dark_svg.svg"))
light_square = load_svg(os.path.join(BOARD_PATH, "square brown light_svg.svg"))

pieces_images = {
    'wP': load_svg(os.path.join(PIECES_PATH, "w_pawn.svg")),
    'wR': load_svg(os.path.join(PIECES_PATH, "w_rook.svg")),
    'wN': load_svg(os.path.join(PIECES_PATH, "w_knight.svg")),
    'wB': load_svg(os.path.join(PIECES_PATH, "w_bishop.svg")),
    'wQ': load_svg(os.path.join(PIECES_PATH, "w_queen.svg")),
    'wK': load_svg(os.path.join(PIECES_PATH, "w_king.svg")),
    'bP': load_svg(os.path.join(PIECES_PATH, "b_pawn.svg")),
    'bR': load_svg(os.path.join(PIECES_PATH, "b_rook.svg")),
    'bN': load_svg(os.path.join(PIECES_PATH, "b_knight.svg")),
    'bB': load_svg(os.path.join(PIECES_PATH, "b_bishop.svg")),
    'bQ': load_svg(os.path.join(PIECES_PATH, "b_queen.svg")),
    'bK': load_svg(os.path.join(PIECES_PATH, "b_king.svg")),
}

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Initialize chess engine
chess_engine = chess.Board()

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            square_color = dark_square if (row + col) % 2 == 0 else light_square
            screen.blit(square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = chess_engine.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = pieces_images[piece.symbol()]
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse click to make a move
                pass

        draw_board()
        draw_pieces()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
