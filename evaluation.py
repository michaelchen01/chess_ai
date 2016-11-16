import sys
import chess
import numpy

class Evaluation:

    evaluation_fn = None

    def __init__(self, evaluation_fn):
        if evaluation_fn == "naive":
            self.evaluate = self.naive
        elif evaluation_fn == "shannon":
            self.evalute = self.shannon


    def naive(self, board):
        piece_value = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.color:
                    piece_value += piece.piece_type
                else:
                    piece_value -= piece.piece_type
        return piece_value

    def shannon(self, board):
        return 0