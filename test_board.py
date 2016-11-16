import argparse
import chess
import subprocess as sp
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", type=int,
        help="which algorithm to use: 1 - minimax, 2 - minimax_ab")
    parser.add_argument("--human", action="store_true",
        help="optional flag to allow a player to play against the AI")
    args = parser.parse_args()

    if (args.algorithm == 1) and (args.human):
        print "Starting game with minimax opponent..."
        board = chess.Board()
        
        while not(board.is_game_over()):
            print "\n"
            print "Current Board: "
            print board
            print "\n"

            # human move
            legal_moves = board.legal_moves
            while True:
                try:
                    print legal_moves
                    next_move = input("Enter your next move: ")
                    print "\n"
                    board.push_san(next_move)
                    break
                except NameError:
                    print bcolors.FAIL + "Invalid input. Did you wrap your string in quotes?" + bcolors.ENDC
                except ValueError:
                    print bcolors.FAIL + "Invalid move. Please choose a move that is in the list of legal moves." + bcolors.ENDC

            # AI move

    else:
        print "Not ready yet!"  