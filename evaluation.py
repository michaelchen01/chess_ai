import evaluation_factors
import sys
import chess
import chess.syzygy


# Piece number to shannon value dictionary
piece_svalue_dict = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 0}
central_squares =   [chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D4, chess.D5, chess.D6,
                    chess.E3, chess.E4, chess.E5, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6]

tablebases = chess.syzygy.open_tablebases()

# 0 = early game
# 1 = middle game
# 2 = late game
def game_stage(board):
    piece_count = sum([1 for square in chess.SQUARES if board.piece_at(square)])
    if piece_count > 28:
        return 0
    elif piece_count > 12:
        return 1
    else:
        return 2

# Adds a huge bonus for checkmate moves
def checkmate_score(board):
    # If it's checkmate, and the player wins
    if board.is_checkmate():
        if (board.turn and board.result()[0] == 1) or (not(board.turn) and board.result()[0] == 0):
            return 20000
        else:
            return -20000
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
    bonuses += 100 if piece_counts[1] == 2 else 0
    # Both bishop bonus
    bonuses += 100 if piece_counts[2] == 2 else 0
    # Both rook bonus
    bonuses += 100 if piece_counts[3] == 2 else 0
    # Queen bonus
    bonuses += 100*piece_counts[4]
    return bonuses

# def other_bonuses(board):
#     if 

def postion_score(board):
    position_score = 0
    if board.turn:
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color:
                if piece.piece_type == 1:
                    position_score += evaluation_factors.w_pawn_pos_value[square]
                elif piece.piece_type == 2:
                    position_score += evaluation_factors.w_knight_pos_value[square]
                elif piece.piece_type == 3:
                    position_score += evaluation_factors.w_bishop_pos_value[square]
                elif piece.piece_type == 4:
                    position_score += evaluation_factors.w_rook_pos_value[square]
                elif piece.piece_type == 5:
                    position_score += evaluation_factors.w_queen_pos_value[square]
                else:
                    position_score += evaluation_factors.w_king_midgame_pos_value[square]
    else:
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and not(piece.color):
                if piece.piece_type == 1:
                    position_score += evaluation_factors.b_pawn_pos_value[square]
                elif piece.piece_type == 2:
                    position_score += evaluation_factors.b_knight_pos_value[square]
                elif piece.piece_type == 3:
                    position_score += evaluation_factors.b_bishop_pos_value[square]
                elif piece.piece_type == 4:
                    position_score += evaluation_factors.b_rook_pos_value[square]
                elif piece.piece_type == 5:
                    position_score += evaluation_factors.b_queen_pos_value[square]
                else:
                    position_score += evaluation_factors.b_king_midgame_pos_value[square]
    return position_score

def mobility_bonus(board):
    return len(board.legal_moves)

def aggression_bonus(board):
    aggression_bonus = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and (piece.color == board.turn):
            aggression_bonus += len(board.attacks(square))
    return aggression_bonus

def double_pawn_penalty(board):
    double_pawn_penalty = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and (piece.color == board.turn) and (square+8 < 64):
            piece_ahead = board.piece_at(square+8)
            if piece_ahead and piece_ahead.piece_type == 1:
                double_pawn_penalty += 1
    return double_pawn_penalty

def pin_penalty(board):
    pin_penalty = 0
    for square in chess.SQUARES:
        if board.is_pinned(board.turn, square):
            pin_penalty += 1
    return pin_penalty

def open_knight_penalty(board):
    pawn_count = 0
    knight_count = 0
    # Find all counts of friendly pawns and knights
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and (piece.color == board.turn):
            if piece.piece_type == 1:
                pawn_count += 1
            if piece.piece_type == 2:
                knight_count += 1
    # Generate the value of the knights
    total_k_val = knight_count*piece_svalue_dict[chess.KNIGHT]
    # Return the pawn-scaled knight value
    return total_k_val*(1.0 - pawn_count/8.0)

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
        # Add Positive Scores
        board_value += checkmate_score(board)
        board_value += material_score(board)
        board_value += piece_bonuses(board)
        board_value += postion_score(board)
        board_value += 0.5*mobility_bonus(board)
        board_value += 0.5*aggression_bonus(board)

        # Subtract penalties
        board_value -= double_pawn_penalty(board)
        board_value -= pin_penalty(board)
        board_value -= 0.1*open_knight_penalty(board)

        # Take into account attacking ability
        return board_value
