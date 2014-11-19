from awale.core import valid_moves_indices


def next_move(game, score, player_id, mvs):
    valid_moves = valid_moves_indices(game, player_id)
    small = min(game[i] for i in valid_moves)
    move = next(
        i for i, a in enumerate(game)
        if (i in valid_moves) and (a == small)
    )
    return move+1
