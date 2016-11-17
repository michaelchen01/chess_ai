from evaluation import Evaluation
import argparse
import chess
import chess_algos
import subprocess as sp
import sys
import terminaltables

piece_dict = {"P": "Pawn", "N": "Knight", "B": "Bishop",
              "R": "Rook", "Q": "Queen",  "K": "King",
              "p": "Pawn", "n": "Knight", "b": "Bishop",
              "r": "Rook", "q": "Queen",  "k": "King"}

parser = argparse.ArgumentParser()
parser.add_argument("algorithm", type=int,
    help="which algorithm to use: 1 - minimax, 2 - minimax_ab")
parser.add_argument("--human", action="store_true",
    help="optional flag to allow a player to play against the AI")
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

if __name__ == "__main__":
    if (args.algorithm == 1) and (args.human):
        print bcolors.OKBLUE + "Starting game with minimax opponent..." + bcolors.ENDC
        board = chess.Board()
        random_algo = chess_algos.Random()
        minimax_algo = chess_algos.Minimax(4, True)

        while not(board.is_game_over()):
            print bcolors.HEADER + "Current Board:" + bcolors.ENDC
            print board
            print "\n"

            # human move
            legal_moves = board.legal_moves

            while True:
                try:
                    # player moves
                    # print_moves(board, legal_moves)
                    # next_move = raw_input("Enter your next move: ")
                    # print "\n"
                    # board.push_uci(next_move)

                    next_move = minimax_algo.next_move(board)
                    print "Computer 1 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                    print bcolors.HEADER + "Current Board:" + bcolors.ENDC
                    print board
                    print "\n"

                    if board.is_game_over():
                        print "Game Over: " + str(board.result())
                        break

                    next_move = minimax_algo.next_move(board)
                    print "Computer 2 makes: " + next_move.uci()
                    board.push_uci(next_move.uci())

                    break
                except NameError:
                    print bcolors.FAIL + "Invalid input. Did you wrap your string in quotes?" + bcolors.ENDC
                except ValueError:
                    print bcolors.FAIL + "Invalid move. Please choose a move that is in the list of legal moves." + bcolors.ENDC

        print "Game Over: " + str(board.result())


    else:
        print "Not ready yet!"  