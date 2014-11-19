import random


def next_move(game, score, player_id, valid_moves, **options):
    play = random.choice(
        valid_moves
    )
    return play
