import sys
import chess
import chess.syzygy

# Piece number to shannon value dictionary
piece_svalue_dict = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 0}
central_squares =   [chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D4, chess.D5, chess.D6,
                    chess.E3, chess.E4, chess.E5, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6]

tablebases = chess.syzygy.open_tablebases()

# Adds a huge bonus for checkmate moves
def checkmate_score(board):
    # If it's checkmate, and the player wins
    if board.is_checkmate():
        if (board.turn and board.result()[0] == 1) or (not(board.turn) and board.result()[0] == 0):
            return 1000000
        else:
            return -1000000
    else:
        return 0

def material_score(board):
    material_value = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_value = piece_svalue_dict[piece.piece_type]
            material_value += piece_value if piece.color == board.turn else -piece_value
    return material_value

def piece_bonuses(board):
    bonuses = 0
    piece_counts = [0]*6
    # Loop over squares and get counts
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and (piece.color == board.turn):
            piece_counts[piece.piece_type-1] += 1
    # Calculate the bonuses
    # Both knight bonus
    bonuses += piece_counts[1]
    # Both bishop bonus
    bonuses += piece_counts[2]
    # Both rook bonus
    bonuses += piece_counts[3]
    # Queen bonus
    bonuses += piece_counts[4]
    return bonuses


# def other_bonuses(board):
#     if 


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
        # Add Material Score
        board_value += checkmate_score(board)
        board_value += material_score(board)
        board_value += piece_bonuses(board)

        piece_count = 0
        # First calculate the score from pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                attack_value = len(board.attacks(square)) if (piece.color == board.turn) else -len(board.attacks(square))
                center_value = 10 if (square in central_squares) and (piece.color == board.turn) else 0

                board_value += 0.1*attack_value
                board_value += center_value

                piece_count += 1

        # Now calculate the move mobility, etc
        new_board = board.copy()
        new_board.turn = not(new_board.turn)

        # board_value += 10*(len(board.legal_moves) - len(new_board.legal_moves))

        if piece_count <= 6:
            wdl = tablebases.probe_wdl(board)
            if wdl != None:
                board_value *= 100*wdl

        # Take into account attacking ability
        return board_value
