from functools import partial
from itertools import groupby
from awale.core import count_stones, game_over, next_valid_states, player_id, \
    other_player
import concurrent.futures


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
                          is_over, valid_states, alpha):
    if is_over:
        alpha = 1  # force to count stones ingame
    s = scores[player] \
        + (alpha * count_stones(game, player))


    # s = scores[player] \
    #     - (alpha * empty_chain_length(game, player)) \
    #     + (alpha * count_stones(game, player))\
    #     + (alpha * len(valid_states))

    return s


def player_evaluation(game, scores, current_player,
                      is_over, valid_states, alpha):
    f = partial(evaluate_player_score,
                game=game, scores=scores, is_over=is_over,
                valid_states=valid_states, alpha=alpha)

    s = f(player=current_player) - f(player=other_player(current_player))

    if is_over:
        s *= 1000
    return s

def min_max(current_player, depth, alpha, state):
    game, scores, player = state
    vs = next_valid_states(game, scores, player)
    is_over = game_over(game, scores, player, vs)
    if depth <= 0 or is_over:
        return -1, player_evaluation(game, scores, current_player,
                                     is_over, vs, alpha)
    else:
        min_or_max = max if player == current_player else min
        res = min_or_max(
            (
                (i, min_max(state=state,
                            depth=depth-1,
                            current_player=current_player,
                            alpha=alpha)[1])
                for i, state in vs
            ),
            key=lambda x: x[1]
        )
        return res


def min_max_h(player_id, depth, alpha, i, state):
    return i, min_max(player_id, depth, alpha, state)[1]


def next_move(game, scores, player_id, mvs, alpha, depth, **options):

    if depth <= 1:
        return min_max(player_id, depth, alpha, (game, scores, player_id))[0] + 1
    else:
        min_max_p = partial(min_max_h, player_id, depth-1, alpha)
        vs = next_valid_states(game, scores, player_id)
        vs_args = zip(*vs)

        with concurrent.futures.ProcessPoolExecutor(len(vs)) as executor:
            res = executor.map(
                min_max_p,
                *vs_args
            )
            return max(res, key=lambda x: x[1])[0] + 1


