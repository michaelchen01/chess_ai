from random import randint
import chess
import csv
import evaluation
import numpy
import sys
import time


naive_evalfn = evaluation.Evaluation("naive")
shannon_evalfn = evaluation.Evaluation("shannon")

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
    """Keeps a hash of board positions seen before"""
    board_hash = {}


    def __init__(self, depth=3, alphabeta=False):
        self.depth = depth
        self.alphabeta = alphabeta

    def next_move(self, board):
        if self.alphabeta:
            return self.calculate_move_ab(board, 0, self.depth, -sys.maxint, sys.maxint)[1]
        else:
            return self.calculate_move_naive(board, 0, self.depth)[1]

    def move_value(self, board, player, move, depth, alpha, beta):
        new_board = board.copy()
        new_board.push_uci(move.uci())

        next_move_value = None
        if new_board.fen() in self.board_hash:
            next_move_value = self.board_hash[new_board.fen()]
        else:
            if player == 0:
                # Get the next move value and move
                next_move_value = self.calculate_move_ab(
                    new_board, player+1, depth-1,
                    alpha, beta)[0]
            else:
                # Get the next move value and move
                next_move_value = self.calculate_move_ab(
                    new_board, player-1, depth-1,
                    alpha, beta)[0]
            self.board_hash[new_board.fen()] = next_move_value

        return next_move_value

    def calculate_move_ab(self, board, player, depth, alpha, beta):
        """ Perform minimax step for Player player on Board board
            and return the optimal move"""
        if depth == 0:
            return (shannon_evalfn.evaluate(board), None)
        if player == 0:
            new_alpha = alpha
            new_beta = beta

            evaluation_max = (-sys.maxint, None)
            legal_moves = board.legal_moves
            # Loop through and recurisvely find the best move,
            # using a certain evaluation function
            for move in legal_moves:
                next_move_value = self.move_value(board, player, move, 
                    depth, new_alpha, new_beta)

                # Set the max as needed
                if next_move_value > evaluation_max[0]:
                    evaluation_max = (next_move_value, move)

                new_alpha = max(new_alpha, evaluation_max[0])
                if new_beta < new_alpha:
                    break

            return evaluation_max
        else:
            new_alpha = alpha
            new_beta = beta

            evaluation_min = (sys.maxint, None)
            legal_moves = board.legal_moves
            # Loop through and recurisvely find the best move,
            # using a certain evaluation function
            for move in legal_moves:
                next_move_value = self.move_value(board, player, move,
                    depth, new_alpha, new_beta)

                # Set the min as needed
                if next_move_value < evaluation_min[0]:
                    evaluation_min = (next_move_value, move)

                new_beta = min(new_beta, evaluation_min[0])
                if new_beta < new_alpha:
                    break
            return evaluation_min


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
                next_move_value = self.calculate_move_naive(
                    new_board,
                    player+1, depth-1)[0]
                # Set the max as needed
                if next_move_value > evaluation_max[0]:
                    evaluation_max = (next_move_value, move)
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
                next_move_value = self.calculate_move_naive(
                    new_board,
                    player-1, depth-1)[0]
                # Set the max as needed
                if next_move_value < evaluation_min[0]:
                    evaluation_min = (next_move_value, move)
            return evaluation_min

class Negamax:

    board_hash = {}

    def __init__(self, depth=3):
        self.depth = depth
        self.prev_best_moves = [None]*self.depth

    def reset_caches(self):
        self.prev_best_moves = [None]*self.depth

    def next_move(self, board):
        # Reset the prev best moves and other caches
        self.reset_caches()
        # Get the start time for the move
        start_time = time.time()
        evaluation_best = (-sys.maxint, None)
        for iter_depth in range(1,self.depth):
            print "Thinking " + str(iter_depth) + " move(s) ahead."
            if time.time() - start_time > 60:
                break
            evaluation_temp = self.calculate_move(board, 1, iter_depth, -sys.maxint, sys.maxint, start_time)
            if evaluation_temp[0] > evaluation_best[0]:
                evaluation_best = evaluation_temp
                self.prev_best_moves[self.depth - iter_depth] = evaluation_temp[1]

        print "Move made in " + str(time.time() - start_time) + " seconds."
        return evaluation_best[1]

    def calculate_move(self, board, player, depth, alpha, beta, start_time):
        if depth == 0 or board.is_game_over() or ((time.time() - start_time) > 60):
            return (shannon_evalfn.evaluate(board), None)
        new_alpha = alpha
        new_beta = beta
        evaluation_best = (-sys.maxint, None)

        move_list = self.order_moves(board, depth)

        for move in move_list:
            new_board = board.copy()
            new_board.push_uci(move.uci())

            next_move_value = -self.calculate_move(new_board, -player, depth-1, -new_beta, -new_alpha, start_time)[0]
            if next_move_value > evaluation_best[0]:
                evaluation_best = (next_move_value, move)
            new_alpha = max(new_alpha, next_move_value)
            if new_alpha >= new_beta:
                break
        return evaluation_best

    def order_moves(self, board, depth):
        prev_best_move = self.prev_best_moves[self.depth - depth]
        # Put the mvoes in a regular list
        move_list = [move for move in board.legal_moves]
        # Put the best move for that node level at the front
        # Check if the move as has been populated
        if prev_best_move != None and prev_best_move in move_list:
            move_list.insert(0, move_list.pop(move_list.index(prev_best_move)))
        return move_list


        return []

class Negascout:

    board_hash = {}

    def __init__(self, depth=3):
        self.depth = depth

    def next_move(self, board):
        return self.calculate_move(board, 1, self.depth, -sys.maxint, sys.maxint)

    def calculate_move(self, board, player, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return (player*shannon_evalfn.evaluate(board), None)

        child_index = 0
        new_alpha = -sys.maxint
        new_beta = sys.maxint
        evaluation_best = (-sys.maxint, None)
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push_uci(move.uci())

            if child_indedx > 0:
                new_move_value = -self.calculate_move(new_board, -player, depth-1, -new_alpha-1, -new_alpha)[0]
                if new_move_value > new_alpha and new_move_value < new_beta:
                    new_move_value = -self.calculate_move(new_board, -player, depth-1, -new_beta, -new_move_value)[0]
            else:
                new_move_value = -self.calculate_move(new_board, -player, depth-1, -new_beta, -new_alpha)[0]
            new_alpha = max(new_alpha, next_move_value)
            if new_alpha >= new_beta:
                break
        return evaluation_best



