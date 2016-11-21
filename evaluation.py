import sys
import chess
import chess.syzygy

# Piece number to shannon value dictionary
piece_svalue_dict = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 20000}
central_squares =   [chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D4, chess.D5, chess.D6,
                    chess.E3, chess.E4, chess.E5, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6]

tablebases = chess.syzygy.open_tablebases()

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
                center_value = 1 if (square in central_squares) and (piece.color == board.turn) else -1

                board_value += piece_value
                board_value += attack_value
                board_value += center_value

        # Now calculate the move mobility, etc
        new_board = board.copy()
        new_board.turn = not(new_board.turn)

        board_value += 10*(len(board.legal_moves) - len(new_board.legal_moves))

        # Take into account attacking ability
        return board_value
