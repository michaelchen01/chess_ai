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

unicode_piece_dict = {"p": u'\u2659', "n": u'\u2658', "b": u'\u2657',
                      "r": u'\u2656', "q": u'\u2655', "k": u'\u2654',
                      "P": u'\u265F', "N": u'\u265E', "B": u'\u265D',
                      "R": u'\u265C', "Q": u'\u265B', "K": u'\u265A'}

parser = argparse.ArgumentParser()
parser.add_argument("white_moves_ahead", type=int,
    help = "number of moves ahead that white thinks")
parser.add_argument("black_moves_ahead", type=int,
    help = "number of moves ahead that black thinks")
parser.add_argument("--human", action="store_true",
    help="optional flag to allow a player to play against the AI")
parser.add_argument("--minimax", action="store_true",
    help="optional flag to allow usage of minimax; random moves are default")
parser.add_argument("--negamax", action="store_true",
    help="optional flag to allow usage of negamax; random moves are default")
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

def print_board(board):
    print bcolors.HEADER + "Current Board:" + bcolors.ENDC
    print board2string(board)
    print "\n"

if __name__ == "__main__":
    board = chess.Board()

    algo = None
    if args.minimax:
        algo_w = chess_algos.Minimax(args.white_moves_ahead, True)
        algo_b = chess_algos.Minimax(args.black_moves_ahead, True)
    elif args.negamax:
        algo_w = chess_algos.Negamax(args.white_moves_ahead)
        algo_b = chess_algos.Negamax(args.black_moves_ahead)
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
                        next_move = algo_w.next_move(board)
                    print "Computer 1 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                print_board(board)

                if board.is_game_over():
                    break

                next_move = None
                if args.exploration and random.random() < 0.1:
                    next_move = chess_algos.Random().next_move(board)
                else:
                    next_move = algo_b.next_move(board)
                print "Computer 2 makes: " + next_move.uci()
                board.push_uci(next_move.uci())

                break
            except NameError:
                print bcolors.FAIL + "Invalid input. Did you wrap your string in quotes?" + bcolors.ENDC
            except ValueError:
                print bcolors.FAIL + "Invalid move. Please choose a move that is in the list of legal moves." + bcolors.ENDC

    print "Game Over: " + str(board.result())

