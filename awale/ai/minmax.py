from itertools import groupby
from awale.core import count_stones, game_over, next_valid_states, player_id


def empty_chain_length(game, player):
    g = [
        m for i, m in enumerate(game)
        if player == player_id(game, i) and m == 0
    ]

    try:
        return max(len(list(l)) for grp, l in groupby(g) if grp == 0)
    except ValueError:
        # no empty seq
        return 0


def evaluate_player_score(game, scores, player,
                          is_over, valid_states, alpha=0):
    if is_over:
        alpha = 1  # force to count stones ingame
    return scores[player]\
        - (alpha * empty_chain_length(game, player))  # malus for
        # + (alpha * count_stones(game, player))\
        # + (alpha * len(valid_states))\


def min_max(game, scores, player, depth, current_player, alpha):
    vs = next_valid_states(game, scores, player)
    is_over = game_over(game, scores, player, vs)
    if depth <= 0 or is_over:
        return -1, evaluate_player_score(game, scores, player,
                                         is_over, vs, alpha)
    else:
        min_or_max = max if player == current_player else min

        return min_or_max(
            (
                (i, min_max(*state,
                            depth=depth-1,
                            current_player=current_player,
                            alpha=alpha)[1])
                for i, state in vs
            ),
            key=lambda x: x[1]
        )


def next_move(game, scores, player_id, mvs, alpha, depth, **options):
    return min_max(game, scores, player_id, depth, player_id, alpha)[0] + 1
