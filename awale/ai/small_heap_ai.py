from awale.core import next_valid_states


def next_move(game, score, player_id, mvs, **options):
    valid_moves = [i for i, s in next_valid_states(game, score, player_id)]
    small = min(game[i] for i in valid_moves)
    move = next(
        i for i, a in enumerate(game)
        if (i in valid_moves) and (a == small)
    )
    return move+1
