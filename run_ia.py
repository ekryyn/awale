import sys
from awale.ai import random_ai, minmax, small_heap_ai
import argparse

def block_until_line(stream):
    ln = ''
    while not ln:
        ln = stream.readline()
    return ln


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", default='random')
    parser.add_argument("--alpha", default=1, type=int)

    strategies = {
        'random': random_ai,
        'small': small_heap_ai,
        'minmax': minmax,
    }

    options = vars(parser.parse_args())

    strategy = strategies[options['s']]

    running = True
    while running:
        # read 4 lines to get information
        game = block_until_line(sys.stdin)
        scores = block_until_line(sys.stdin)
        to_play = block_until_line(sys.stdin)
        valid_moves = block_until_line(sys.stdin)

        # transform values to suitable representation
        game = [int(a) for a in game.split(' ')]
        scores = [int(a) for a in scores.split(' ')]
        to_play = int(to_play) - 1

        try:
            valid_moves = [int(a) for a in valid_moves.split(' ')]
        except ValueError:
            sys.stderr.write("No valid move :/\n")
            from awale.gui.console import display_game
            sys.stderr.write(display_game(game, scores) + "\n")
            running = False

        print strategy.next_move(game, scores, to_play, valid_moves, **options)
        sys.stdout.flush()
