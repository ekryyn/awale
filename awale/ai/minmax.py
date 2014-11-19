from awale.core import next_state, valid_moves_indices, count_stones, game_over


def next_valid_states(game, scores, player):
    return [
        (i, next_state(game, scores, player, i))
        for i in valid_moves_indices(game, player)
    ]


def evaluate_player_score(game, scores, player, is_over, alpha=0):
    if is_over:
        alpha = 1  # force to count stones ingame
    return scores[player] + (alpha * count_stones(game, player))


def min_max(game, scores, player, depth, current_player, alpha):
    is_over = game_over(game, scores, player)
    if depth <= 0 or is_over:
        return -1, evaluate_player_score(game, scores, player, is_over, alpha)
    else:
        min_or_max = max if player == current_player else min

        return min_or_max(
            (
                (i, min_max(*state,
                            depth=depth-1,
                            current_player=current_player,
                            alpha=alpha)[1])
                for i, state in next_valid_states(game, scores, player)
            ),
            key=lambda x: x[1]
        )



def next_move(game, scores, player_id, mvs, alpha, **options):
    return min_max(game, scores, player_id, 4, player_id, alpha)[0] + 1
