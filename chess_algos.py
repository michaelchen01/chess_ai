import sys
import numpy
import chess
import evaluation
from random import randint

naive_evalfn = evaluation.Evaluation("naive")

class Random:

    def next_move(self, board):
        legal_moves = board.legal_moves
        random_move = randint(1, len(legal_moves))
        # Can't directly access moves by index, so iterate
        move_index = 0
        for move in legal_moves:
            if move_index == (random_move - 1):
                return move
            else:
                move_index += 1


class Minimax:

    """Maximum depth on minimax search"""
    depth = 0
    """Enable or disable alphabeta pruning"""
    alphabeta = False

    def __init__(self, depth=2, alphabeta=False):
        self.depth = depth
        self.alphabeta = False

    def next_move(self, board):
        return self.calculate_move_naive(board, 0, self.depth)[1]

    def calculate_move_naive(self, board, player, depth):
        """ Perform minimax step for Player player on Board board
            and return the optimal move"""
        if depth == 0 or board.is_game_over():
            return (naive_evalfn.evaluate(board), None)
        if player == 0:
            evaluation_max = (-sys.maxint, None)
            legal_moves = board.legal_moves
            # Loop through and recurisvely find the best move,
            # using a certain evaluation function
            for move in legal_moves:
                new_board = board.copy()
                new_board.push_uci(move.uci())
                # Get the next move value and move
                next_move_value = self.calculate_move(
                    new_board,
                    player+1, depth-1)[0]
                # Set the max as needed
                if next_move_value > evaluation_max[0]:
                    evaluation_max = (next_move_value, move)
            print evaluation_max
            return evaluation_max
        else:
            evaluation_min = (sys.maxint, None)
            legal_moves = board.legal_moves
            # Loop through and recurisvely find the best move,
            # using a certain evaluation function
            for move in legal_moves:
                new_board = board.copy()
                new_board.push_uci(move.uci())
                # Get the next move value and move
                next_move_value = self.calculate_move(
                    new_board,
                    player-1, depth-1)[0]
                # Set the max as needed
                if next_move_value < evaluation_min[0]:
                    evaluation_min = (next_move_value, move)
            print evaluation_min
            return evaluation_min
