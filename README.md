## Synopsis

This is a simple chess AI project written in Python for CS 182 that contains both the engine and a simple console UI. 

## Requirements

This project relies on the python-chess and numpy packages, which can both be obtained using `pip install [package-name]`.

## Installation

Installation is simple, just clone the project to a directory of your choice.

## Usage

```usage: test_board.py [-h] [--human] [--minimax] [--negamax] [--exploration]
                     white_moves_ahead black_moves_ahead

positional arguments:
  white_moves_ahead  number of moves ahead that white thinks
  black_moves_ahead  number of moves ahead that black thinks

optional arguments:
  -h, --help         show this help message and exit
  --human            optional flag to allow a player to play against the AI
  --minimax          optional flag to allow usage of minimax; random moves are
                     default
  --negamax          optional flag to allow usage of negamax; random moves are
                     default. cannot be combined with minimax.
  --exploration      optional flag to allow an AI to make a random move with
                     small probability```

## Contributors

Michael Chen