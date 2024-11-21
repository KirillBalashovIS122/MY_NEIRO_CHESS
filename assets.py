import pygame
import os
import cairosvg
from PIL import Image
from io import BytesIO

class Assets:
    def __init__(self, screen):
        self.screen = screen
        self.SQUARE_SIZE = screen.get_width() // 8
        self.load_assets()

    def load_svg(self, path):
        with open(path, "rb") as svg_file:
            svg_data = svg_file.read()
        png_data = cairosvg.svg2png(bytestring=svg_data, output_width=self.SQUARE_SIZE, output_height=self.SQUARE_SIZE)
        png_file = Image.open(BytesIO(png_data)).convert("RGBA")
        return pygame.image.fromstring(png_file.tobytes(), png_file.size, png_file.mode)

    def load_assets(self):
        ASSETS_PATH = "/home/kbalashov/VS_Code/MY_NEIRO_CHESS/assets"
        BOARD_PATH = os.path.join(ASSETS_PATH, "board")
        PIECES_PATH = os.path.join(ASSETS_PATH, "pieces")

        self.dark_square = self.load_svg(os.path.join(BOARD_PATH, "square brown dark_svg.svg"))
        self.light_square = self.load_svg(os.path.join(BOARD_PATH, "square brown light_svg.svg"))

        self.pieces_images = {
            'P': self.load_svg(os.path.join(PIECES_PATH, "w_pawn.svg")),
            'R': self.load_svg(os.path.join(PIECES_PATH, "w_rook.svg")),
            'N': self.load_svg(os.path.join(PIECES_PATH, "w_knight.svg")),
            'B': self.load_svg(os.path.join(PIECES_PATH, "w_bishop.svg")),
            'Q': self.load_svg(os.path.join(PIECES_PATH, "w_queen.svg")),
            'K': self.load_svg(os.path.join(PIECES_PATH, "w_king.svg")),
            'p': self.load_svg(os.path.join(PIECES_PATH, "b_pawn.svg")),
            'r': self.load_svg(os.path.join(PIECES_PATH, "b_rook.svg")),
            'n': self.load_svg(os.path.join(PIECES_PATH, "b_knight.svg")),
            'b': self.load_svg(os.path.join(PIECES_PATH, "b_bishop.svg")),
            'q': self.load_svg(os.path.join(PIECES_PATH, "b_queen.svg")),
            'k': self.load_svg(os.path.join(PIECES_PATH, "b_king.svg")),
        }
