# coding: utf-8
from itertools import cycle, islice, takewhile
from functools import partial


def next_valid_states(game, scores, player):
    can_play_ = partial(can_play, game, scores, player)
    indexed_can_play = (
        (index, can_play_(index)) for index, amount in enumerate(game)
    )
    return [
        (i, next_state)
        for i, (playable, next_state) in indexed_can_play
        if playable
    ]


def is_starving(player, game):
    """
    return True if player has no stone
    False if he has one or more
    """
    stones = sum(
        a for i, a in enumerate(game)
        if player == player_id(game, i)
    )
    return stones == 0


def game_over(game, scores, current_player, valid_states_cache=None):
    vs = valid_states_cache or next_valid_states(game, scores, current_player)
    can_move = bool(len(vs))
    return any(s >= 25 for s in scores) \
        or not can_move \
        or sum(game) <= 6


def other_player(current):
    return 0 if current else 1


def winner(game, scores):
    # first add remaining stones to score
    for player, _ in enumerate(scores):
        scores[player] += count_stones(game, player)

    # then compare
    if scores[0] == scores[1]:
        return None
    elif scores[0] > scores[1]:
        return 0
    else:
        return 1


def count_stones(game, player):
    return sum(a for i, a in enumerate(game) if player_id(game, i) == player)


def player_id(game, index):
    """ _index_ belongs to player 0 or 1 """
    l = len(game)/2
    return 0 if index < l else 1


def can_play(game, scores, player, index):
    """ _player_ can play on _index_ """
    after = None, None, None
    if player == player_id(game, index) and game[index]:
        after = next_state(game, scores, player, index)
        return not is_starving(other_player(player), after[0]), after

    return False, after


def can_eat(game, player, index):
    """ player can eat index """
    return (
        1 < game[index] <= 3
        and
        player != player_id(game, index)
    )


def rotate(li, x):
    """ return a list rotated on _x_ """
    return li[-x % len(li):] + li[:-x % len(li)]


def step_game(game, index):
    """ return next game state, and last modified index """
    game = game[:]  # copy
    nb_stone = game[index]
    game[index] = 0

    it = cycle(i for i in range(len(game)) if i != index) # cycle over indexes
    [next(it) for _ in range(index)] # forward until index+1

    for i in islice(it, nb_stone):
        game[i] += 1

    return game, i


def eat_stones(game, last, player, scores):
    """
    return new game and scores after _player_ have eaten stones
    """
    game = game[:]
    scores = scores[:]
    indexes = list(reversed(range(len(game))))
    indexes = rotate(indexes, last + 1)
    eat_predicate = partial(can_eat, game, player)
    to_eat = takewhile(eat_predicate, indexes)
    for i in to_eat:
        scores[player] += game[i]
        game[i] = 0
    return game, scores


def next_state(game, scores, player, index_to_play):
    """
    play the move, eat the stones, and return the state
    """
    game, last_hole = step_game(game, index_to_play)
    game, scores = eat_stones(game, last_hole, player, scores)

    return game, scores, other_player(player)


class AwaleException(Exception): pass


class WrongMove(AwaleException): pass


class GameState(object):
    current_player = 0
    game = [4]*12
    scores = [0, 0]
    letters = dict((l, i) for i, l in enumerate(list("ABCDEFfedcba")))

    def over(self):
        return game_over(self.game, self.scores, self.current_player)

    def current_player_can_play(self, index):
        return can_play(self.game, self.scores, self.current_player, index)[0]

    def play_index(self, index):
        if not self.current_player_can_play(index):
            raise WrongMove("You can't play this !")

        # play
        self.game, self.scores, self.current_player = next_state(
            self.game, self.scores, self.current_player, index
        )

    def play(self, player, letter):
        if player != self.current_player:
            raise AwaleException("This is not your turn !")

        try:
            index = self.letters[letter]
        except KeyError:
            raise WrongMove("%s is not a valid move." % letter)

        self.play_index(player, index)

