import chess
import chess.svg

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        try:
            self.board.push_uci(move)
        except ValueError:
            return False
        return True

    def get_legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]

    def is_game_over(self):
        return self.board.is_game_over()

    def get_board_fen(self):
        return self.board.fen()

    def get_board_svg(self):
        return chess.svg.board(self.board)

    def reset(self):
        self.board.reset()
