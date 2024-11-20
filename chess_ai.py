import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import chess

class ChessAI:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = Sequential([
            Flatten(input_shape=(8, 8, 12)),  # 8x8 board, 12 channels (one for each piece type and color)
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(4096, activation='softmax')  # Output layer with one neuron per possible move
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, data, labels, epochs=10):
        self.model.fit(data, labels, epochs=epochs)

    def predict_move(self, board_fen):
        board = chess.Board(board_fen)
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        board_state = self.board_to_input(board)
        predictions = self.model.predict(board_state)
        best_move_index = tf.argmax(predictions, axis=1).numpy()[0]
        return legal_moves[best_move_index].uci()

    def board_to_input(self, board):
        piece_map = board.piece_map()
        board_state = [[[0 for _ in range(12)] for _ in range(8)] for _ in range(8)]
        for square, piece in piece_map.items():
            row = chess.square_rank(square)
            col = chess.square_file(square)
            piece_index = (piece.piece_type - 1) + (6 if piece.color == chess.WHITE else 0)
            board_state[row][col][piece_index] = 1
        return tf.expand_dims(tf.convert_to_tensor(board_state), axis=0)
