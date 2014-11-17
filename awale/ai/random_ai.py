import random


def next_move(game, score, player_id, valid_moves):
    play = random.choice(
        valid_moves
    )
    return play
