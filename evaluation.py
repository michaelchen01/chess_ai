import sys
import chess

# Piece number to shannon value dictionary
piece_svalue_dict = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 1000}


class Evaluation:

    evaluation_fn = None

    def __init__(self, evaluation_fn):
        if evaluation_fn == "naive":
            self.evaluate = self.naive
        elif evaluation_fn == "shannon":
            self.evaluate = self.shannon

    def naive(self, board):
        board_value = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_value = piece.piece_type if piece.color else -piece.piece_type
                board_value += piece_value
        return board_value

    def shannon(self, board):
        board_value = 0
        # First calculate the score from pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                shannon_value = piece_svalue_dict[piece.piece_type]
                piece_value = shannon_value if (piece.color == board.turn) else -shannon_value
                attack_value = len(board.attacks(square)) if (piece.color == board.turn) else -len(board.attacks(square))
                board_value += piece_value
                board_value += 0.05*attack_value

        # Now calculate the move mobility, etc
        new_board = board.copy()
        new_board.turn = not(new_board.turn)
        board_value += 0.1*(len(board.legal_moves) - len(new_board.legal_moves))

        # Take into account attacking ability

        return board_value
