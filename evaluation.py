import sys
import chess


class Evaluation:

    evaluation_fn = None

    def __init__(self, evaluation_fn):
        if evaluation_fn == "naive":
            self.evaluate = self.naive
        elif evaluation_fn == "shannon":
            self.evalute = self.shannon

    def naive(self, board):
        board_value = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_value = piece.piece_type if piece.color else -piece.piece_type
                board_value += piece_value
        return board_value

    def shannon(self, board):
        return 0
