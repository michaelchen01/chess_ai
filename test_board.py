from evaluation import Evaluation
import argparse
import chess
import chess_algos
import subprocess as sp
import random
import sys
import terminaltables

piece_dict = {"P": "Pawn", "N": "Knight", "B": "Bishop",
              "R": "Rook", "Q": "Queen",  "K": "King",
              "p": "Pawn", "n": "Knight", "b": "Bishop",
              "r": "Rook", "q": "Queen",  "k": "King"}

parser = argparse.ArgumentParser()
parser.add_argument("--human", action="store_true",
    help="optional flag to allow a player to play against the AI")
parser.add_argument("--minimax", action="store_true",
    help="optional flag to allow usage of minimax; random moves are default")
parser.add_argument("--negamax", action="store_true",
    help="optional flag to allow usage of negamax; random moves are default")
parser.add_argument("--negascout", action="store_true",
    help="optional flag to allow usage of negascout; random moves are default")
parser.add_argument("--exploration", action="store_true",
    help="optional flag to allow an AI to make a random move with small probability")
args = parser.parse_args()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_moves(board, legal_moves):
    print bcolors.HEADER + "Possible Moves" + bcolors.ENDC

    move_dict = {}
    for move in legal_moves:
        piece_name = board.piece_at(move.from_square).symbol()
        if piece_dict[piece_name] in move_dict:
            move_dict[piece_dict[piece_name]].append(move.uci())
        else:
            move_dict[piece_dict[piece_name]] = [move.uci()]

    table_data = []
    table_data.append(['Piece', 'Moves'])
    for key in move_dict:
        table_data.append([key, ", ".join(move_dict[key])])
    table = terminaltables.AsciiTable(table_data)
    print table.table

def print_board(board):
    print bcolors.HEADER + "Current Board:" + bcolors.ENDC
    print board
    print "\n"

if __name__ == "__main__":
    board = chess.Board()

    algo = None
    if args.minimax:
        algo = chess_algos.Minimax(4, True)
    elif args.negamax:
        algo = chess_algos.Negamax(5)
    elif args.negascout:
        algo = chess_algos.Negascout(4)
    else:
        algo = chess_algos.Random()

    while not(board.is_game_over()):
        print_board(board)
        # human move
        legal_moves = board.legal_moves

        while True:
            try:
                if args.human:
                    # player moves
                    print_moves(board, legal_moves)
                    next_move = raw_input("Enter your next move: ")
                    print "\n"
                    board.push_uci(next_move)
                else:
                    next_move = None
                    if args.exploration and random.random() < 0.1:
                        next_move = chess_algos.Random().next_move(board)
                    else:
                        next_move = algo.next_move(board)
                    print "Computer 1 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                print_board(board)

                if board.is_game_over():
                    break

                next_move = None
                if args.exploration and random.random() < 0.1:
                    next_move = chess_algos.Random().next_move(board)
                else:
                    next_move = algo.next_move(board)
                print "Computer 2 makes: " + next_move.uci()
                board.push_uci(next_move.uci())

                break
            except NameError:
                print bcolors.FAIL + "Invalid input. Did you wrap your string in quotes?" + bcolors.ENDC
            except ValueError:
                print bcolors.FAIL + "Invalid move. Please choose a move that is in the list of legal moves." + bcolors.ENDC

    print "Game Over: " + str(board.result())

