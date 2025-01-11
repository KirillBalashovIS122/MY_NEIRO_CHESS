import pygame
import chess
import time
from chess_ai import ChessAI
from assets import Assets
from chess_engine import ChessEngine

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.chess_engine = ChessEngine()
        self.chess_ai = ChessAI()
        self.assets = Assets(screen)
        self.selected_piece = None
        self.move_history = []
        self.move_number = 1

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                square_color = self.assets.dark_square if (row + col) % 2 == 0 else self.assets.light_square
                self.screen.blit(square_color, (col * self.assets.SQUARE_SIZE, row * self.assets.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_engine.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = self.assets.pieces_images[piece.symbol()]
                    self.screen.blit(piece_image, (col * self.assets.SQUARE_SIZE, row * self.assets.SQUARE_SIZE))

    def handle_move(self, start_square, end_square):
        piece = self.chess_engine.board.piece_at(start_square)
        
        if piece is None:
            print("No piece selected")
            return False

        move = chess.Move(start_square, end_square)
        if move in self.chess_engine.board.legal_moves:
            # Проверка на превращение пешки
            if piece.piece_type == chess.PAWN:
                if chess.square_rank(end_square) == 7 or chess.square_rank(end_square) == 0:
                    move.promotion = chess.QUEEN  # Превращение в ферзя

            self.chess_engine.make_move(move.uci())
            move_info = self.format_move_info(piece, start_square, end_square)
            self.move_history.append(move_info)
            print(f"Move executed: {move}")
            self.move_number += 1
            return True
        
        print("Illegal move attempted")
        return False

    def format_move_info(self, piece, start_square, end_square):
        if piece is None:
            return "No piece selected"
        
        piece_symbol = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol().lower()
        start_square_name = chess.square_name(start_square)
        end_square_name = chess.square_name(end_square)

        color = "White" if piece.color == chess.WHITE else "Black"
        return f"{color} {piece_symbol} from {start_square_name} to {end_square_name}"

    def display_turn(self):
        turn_text = f"{'White' if self.chess_engine.board.turn == chess.WHITE else 'Black'}'s Turn"
        font = pygame.font.Font(None, 36)
        text = font.render(turn_text, True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

    def display_move_history(self):
        font = pygame.font.Font(None, 24)
        y_offset = 50
        for i, move in enumerate(self.move_history[-5:]):
            text = font.render(f"{i + 1}: {move}", True, (0, 0, 0))
            self.screen.blit(text, (10, y_offset))
            y_offset += 20

    def display_current_move(self):
        current_move = self.move_history[-1] if self.move_history else ""
        font = pygame.font.Font(None, 36)
        move_text = f"Move {self.move_number}: {current_move}"
        text = font.render(move_text, True, (0, 0, 0))
        self.screen.blit(text, (10, 100))

    def run(self, game_mode, chess_ai=None):
        running = True
        while running:
            if self.chess_engine.is_game_over():
                print("Game Over!")
                running = False
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // self.assets.SQUARE_SIZE
                    row = y // self.assets.SQUARE_SIZE
                    square = chess.square(col, 7 - row)
                    if game_mode == "PvP" or (game_mode == "PvAI" and self.chess_engine.board.turn == chess.WHITE):
                        if self.selected_piece:
                            if self.handle_move(self.selected_piece, square):
                                self.selected_piece = None
                            else:
                                self.selected_piece = square
                        else:
                            self.selected_piece = square

                    if game_mode == "PvAI" and self.chess_engine.board.turn == chess.BLACK:
                        if chess_ai:
                            ai_move = chess_ai.predict_move(self.chess_engine.get_board_fen())
                            if ai_move:
                                self.chess_engine.make_move(ai_move)
                                print(f"AI move: {ai_move}")
                            time.sleep(1)

            self.draw_board()
            self.draw_pieces()
            self.display_turn()
            self.display_move_history()
            self.display_current_move()
            pygame.display.flip()

        self.chess_engine.reset()
