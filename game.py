import pygame
import chess
import time
from chess_ai import ChessAI
from assets import Assets

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.chess_engine = chess.Board()
        self.chess_ai = ChessAI()
        self.assets = Assets(screen)
        self.selected_piece = None

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                square_color = self.assets.dark_square if (row + col) % 2 == 0 else self.assets.light_square
                self.screen.blit(square_color, (col * self.assets.SQUARE_SIZE, row * self.assets.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_engine.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = self.assets.pieces_images[piece.symbol()]
                    self.screen.blit(piece_image, (col * self.assets.SQUARE_SIZE, row * self.assets.SQUARE_SIZE))

    def handle_move(self, start_square, end_square):
        move = chess.Move(start_square, end_square)
        if move in self.chess_engine.legal_moves:
            self.chess_engine.push(move)
            return True
        return False

    def run(self, game_mode):
        running = True
        while running:
            if game_mode == "PvP":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        col = x // self.assets.SQUARE_SIZE
                        row = y // self.assets.SQUARE_SIZE
                        square = chess.square(col, 7 - row)
                        piece = self.chess_engine.piece_at(square)
                        if piece:
                            self.selected_piece = square
                        elif self.selected_piece:
                            if self.handle_move(self.selected_piece, square):
                                self.selected_piece = None
            elif game_mode == "PvAI":
                if self.chess_engine.turn == chess.WHITE:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            col = x // self.assets.SQUARE_SIZE
                            row = y // self.assets.SQUARE_SIZE
                            square = chess.square(col, 7 - row)
                            piece = self.chess_engine.piece_at(square)
                            if piece:
                                self.selected_piece = square
                            elif self.selected_piece:
                                if self.handle_move(self.selected_piece, square):
                                    self.selected_piece = None
                else:
                    ai_move = self.chess_ai.predict_move(self.chess_engine.fen())
                    if ai_move:
                        self.chess_engine.push_uci(ai_move)
                    time.sleep(1)
            elif game_mode == "AIvAI":
                ai_move = self.chess_ai.predict_move(self.chess_engine.fen())
                if ai_move:
                    self.chess_engine.push_uci(ai_move)
                time.sleep(1)

            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

        self.chess_engine.reset()
