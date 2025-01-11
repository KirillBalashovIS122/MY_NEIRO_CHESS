import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input, Conv2D, MaxPooling2D, Dropout, BatchNormalization
import chess
import pandas as pd
import numpy as np
import os
import logging
from tqdm import tqdm  # Для отображения прогресс-бара

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Отключение GPU (если не используется)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class ChessAI:
    def __init__(self):
        self.model = self.build_model()
        try:
            self.model = tf.keras.models.load_model('chess_ai_model.h5')
            logging.info("Loaded saved model.")
        except:
            logging.warning("No saved model found, using a new one.")

    def build_model(self):
        model = Sequential([
            Input(shape=(8, 8, 12)),
            Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='softmax')  # Уменьшено количество классов до 256
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        logging.info("Model built and compiled.")
        return model

    def train(self, data, labels, epochs=20, batch_size=32):
        logging.info("Starting training...")
        history = self.model.fit(data, labels, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=1)
        self.model.save('chess_ai_model.h5')
        logging.info("Training completed and model saved.")
        return history

    def predict_move(self, board_fen):
        board = chess.Board(board_fen)
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            logging.warning("No legal moves available for AI")
            return None

        board_state = self.board_to_input(board)
        predictions = self.model.predict(board_state, verbose=0)
        
        # Сортируем ходы по вероятности
        sorted_indices = np.argsort(predictions[0])[::-1]
        
        # Выбираем первый легальный ход
        for move_index in sorted_indices:
            if move_index < len(legal_moves):
                move = legal_moves[move_index]
                logging.info(f"AI predicted move: {move.uci()}")
                return move.uci()
        
        logging.error("No legal move found in predictions")
        return None

    def board_to_input(self, board):
        piece_map = board.piece_map()
        board_state = np.zeros((8, 8, 12))
        for square, piece in piece_map.items():
            row = chess.square_rank(square)
            col = chess.square_file(square)
            piece_index = (piece.piece_type - 1) + (6 if piece.color == chess.WHITE else 0)
            board_state[row, col, piece_index] = 1
        return tf.expand_dims(board_state, axis=0)

    @staticmethod
    def prepare_data(data):
        """Prepares the dataset for training the model."""
        logging.info("Preparing data...")
        inputs = []
        labels = []

        for _, row in tqdm(data.iterrows(), total=len(data), desc="Processing data"):
            board = chess.Board()
            moves = row['moves'].split()

            for i, move in enumerate(moves[:-1]):
                try:
                    move_uci = ChessAI.san_to_uci(board, move)
                except chess.InvalidMoveError:
                    logging.warning(f"Skipping invalid move: {move}")
                    continue

                board.push_uci(move_uci)
                board_input = ChessAI.board_to_input_static(board)

                next_move = moves[i + 1]
                try:
                    next_move_uci = ChessAI.san_to_uci(board, next_move)
                    legal_moves = list(board.legal_moves)
                    label = legal_moves.index(chess.Move.from_uci(next_move_uci))
                except (chess.InvalidMoveError, ValueError):
                    logging.warning(f"Skipping invalid next move: {next_move}")
                    continue

                inputs.append(board_input)
                labels.append(label)

        inputs = np.array(inputs)
        logging.info(f"Input data shape: {inputs.shape}")
        logging.info(f"Labels length: {len(labels)}")

        # Уменьшение количества классов до 256
        labels = tf.keras.utils.to_categorical(labels, num_classes=256)
        logging.info(f"Labels shape after categorical conversion: {labels.shape}")

        return inputs, labels

    @staticmethod
    def board_to_input_static(board):
        """Static version of board_to_input for dataset processing."""
        piece_map = board.piece_map()
        board_state = np.zeros((8, 8, 12))
        for square, piece in piece_map.items():
            row = chess.square_rank(square)
            col = chess.square_file(square)
            piece_index = (piece.piece_type - 1) + (6 if piece.color == chess.WHITE else 0)
            board_state[row, col, piece_index] = 1
        return board_state

    @staticmethod
    def san_to_uci(board, move):
        """Преобразует ход из SAN (стандартная алгебраическая нотация) в UCI."""
        try:
            move_obj = board.parse_san(move)
            return move_obj.uci()
        except chess.InvalidMoveError:
            raise chess.InvalidMoveError(f"Invalid move: {move}")

# Загрузка датасета
dataset_path = '/home/kbalashov/VS_Code/MY_NEIRO_CHESS/assets/dataset/games.csv'
logging.info(f"Loading dataset from {dataset_path}...")
dataset = pd.read_csv(dataset_path)

# Ограничение размера датасета (например, первые 10 000 строк)
dataset = dataset.head(10000)
logging.info(f"Dataset loaded with {len(dataset)} rows.")

# Подготовка данных для обучения
chess_ai = ChessAI()
data, labels = ChessAI.prepare_data(dataset)

# Обучение модели
chess_ai.train(data, labels, epochs=10)
