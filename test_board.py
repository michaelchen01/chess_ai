# Michael Chen, 2016

# Libraries
from evaluation import Evaluation
import argparse
import chess
import chess_algos
import subprocess as sp
import random
import sys
import terminaltables

# Dictionary mapping from ascii letter to piece name
piece_dict = {"P": "Pawn", "N": "Knight", "B": "Bishop",
              "R": "Rook", "Q": "Queen",  "K": "King",
              "p": "Pawn", "n": "Knight", "b": "Bishop",
              "r": "Rook", "q": "Queen",  "k": "King"}

# Dictionary mapping from ascii letter to unicode symbol for printing
unicode_piece_dict = {"p": u'\u2659', "n": u'\u2658', "b": u'\u2657',
                      "r": u'\u2656', "q": u'\u2655', "k": u'\u2654',
                      "P": u'\u265F', "N": u'\u265E', "B": u'\u265D',
                      "R": u'\u265C', "Q": u'\u265B', "K": u'\u265A'}

# Handles all the commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("white_moves_ahead", type=int,
    help = "number of moves ahead that white thinks")
parser.add_argument("black_moves_ahead", type=int,
    help = "number of moves ahead that black thinks")
parser.add_argument("timeout_in_seconds", type=int,
    help = "number of seconds before move searching times out")
parser.add_argument("--human_white", action="store_true",
    help="optional flag to allow a player to play against the AI")
parser.add_argument("--human_black", action="store_true",
    help="optional flag to allow a player to play against the AI")
parser.add_argument("--minimax", action="store_true",
    help="optional flag to allow usage of minimax; random moves are default")
parser.add_argument("--negamax", action="store_true",
    help="optional flag to allow usage of negamax; random moves are default")
args = parser.parse_args()

# Handles all the commandline output colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Prints the possible moves for a human nicely using terminaltables
def print_moves(board, legal_moves):
    print bcolors.HEADER + "Possible Moves" + bcolors.ENDC

    # Loop through and append possible moves to the terminal table
    move_dict = {}
    for move in legal_moves:
        piece_name = board.piece_at(move.from_square).symbol()
        if piece_dict[piece_name] in move_dict:
            move_dict[piece_dict[piece_name]].append(move.uci())
        else:
            move_dict[piece_dict[piece_name]] = [move.uci()]

    # Format the table
    table_data = []
    table_data.append(['Piece', 'Moves'])
    for key in move_dict:
        table_data.append([key, ", ".join(move_dict[key])])
    table = terminaltables.AsciiTable(table_data)
    # Print the table
    print table.table

# Function extracted from the built in python-chess board,
# modified to print column and row info, and display
# Unicode characters instead of letters
def board2string(board):
    builder = [u'a b c d e f g h\n']
    builder.append(u'----------------\n')

    index = 8
    for square in chess.SQUARES_180:
        piece = board.piece_at(square)

        if piece:
            builder.append(unicode_piece_dict[piece.symbol()])
        else:
            builder.append(".")

        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            if square != chess.H1:
                builder.append(" |" + str(index) + "\n")
                index -= 1
        else:
            builder.append(" ")

    builder.append(" |" + str(index))
    return "".join(builder)

# Wrapper to print the board with the Current Board header
def print_board(board):
    print bcolors.HEADER + "Current Board:" + bcolors.ENDC
    print board2string(board)
    print "\n"

# Main function
if __name__ == "__main__":
    # Initialize the starting board
    board = chess.Board()

    # Checks flags to see which algorithms to use
    algo = None
    if args.minimax:
        # Initializes minimax with input moves ahead and alpha beta activated
        algo_w = chess_algos.Minimax(args.white_moves_ahead, True)
        algo_b = chess_algos.Minimax(args.black_moves_ahead, True)
    elif args.negamax:
        # initializes negamax with input moves ahead and timeout
        algo_w = chess_algos.Negamax(args.white_moves_ahead, args.timeout_in_seconds)
        algo_b = chess_algos.Negamax(args.black_moves_ahead, args.timeout_in_seconds)
    else:
        # PARTY TIME RANDOM ALGO :-)
        algo_w = chess_algos.Random()
        algo_b = chess_algos.Random()

    # Loops until game is over
    while not(board.is_game_over()):
        # Print the starting board
        print_board(board)
        # Calculate the legalmoves for human players
        legal_moves = board.legal_moves

        while True:
            try:
                # Checks if human is playing white
                if args.human_white:
                    # player moves
                    print_moves(board, legal_moves)
                    next_move = raw_input("Enter your next move: ")
                    print "\n"
                    board.push_uci(next_move)
                else:
                    # Otherwise execute the AI move for white
                    next_move = algo_w.next_move(board)
                    print "Computer 1 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                # Print the board between moves
                print_board(board)

                # And check if the game is over after white's move
                if board.is_game_over():
                    break

                # Checks if human is playing black
                if args.human_black:
                    # player moves
                    print_moves(board, legal_moves)
                    next_move = raw_input("Enter your next move: ")
                    print "\n"
                    board.push_uci(next_move)
                else:
                    # Execute AI move for black
                    next_move = algo_b.next_move(board)
                    print "Computer 2 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                break
            # Catch exceptions for bad inputs when playing in human move
            except NameError:
                print bcolors.FAIL + "Invalid input. Did you wrap your string in quotes?" + bcolors.ENDC
            except ValueError:
                print bcolors.FAIL + "Invalid move. Please choose a move that is in the list of legal moves." + bcolors.ENDC
    # Prints the end result of the game
    print "Game Over: " + str(board.result())

