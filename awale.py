# coding: utf-8
from itertools import cycle, islice, takewhile
from functools import partial

def game_over(game, scores):
    return any(s >= 25 for s in scores) or sum(game) <= 6

def winner(scores):
    if scores[0] == scores[1]:
        return None
    elif scores[0] > scores[1]:
        return 0
    else:
        return 1

def player_id(game, index):
    """ _index_ belongs to player 0 or 1 """
    l = len(game)/2
    return 0 if index < l else 1

def can_play(game, player, index):
    """ _player_ can play on _index_ """
    return player == player_id(game, index) and game[index]

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

def display_cell(c):
    return "[%2d]" % c

def display_game(game, scores):
    half = int(len(game)/2)
    p0_line = game[:half]
    p1_line = reversed(game[half:])
    print("                      %s" % "   ".join('abcdef'))
    print("                 |  %s  | <- Player 2 (%2d)" % ("".join(map(display_cell, p1_line)), scores[1]))
    print("(%2d) Player 1 -> |  %s  |" % (scores[0], "".join(map(display_cell, p0_line))))
    print("                      %s" % "   ".join('ABCDEF'))


class AwaleException(Exception): pass

class WrongMove(AwaleException): pass

class GameState(object):
    current_player = 0
    game = [4]*12
    scores = [0, 0]
    letters = dict((l, i) for i, l in enumerate(list("ABCDEFfedcba")))

    def switch_current_player(self):
        self.current_player = 0 if self.current_player else 1

    def play(self, player, letter):
        if player != self.current_player:
            raise AwaleException("This is not your turn !")

        try:
            index = self.letters[letter]
        except KeyError:
            raise WrongMove("%s is not a valid move." % letter)

        if not can_play(self.game, player, index):
            raise WrongMove("You can't play this !")

        # play
        self.game, last = step_game(self.game, index)
        # eat
        self.game, self.scores = eat_stones(self.game, last, player, self.scores)
        # switch turn
        self.switch_current_player()

    def display(self):
        display_game(self.game, self.scores)


g = GameState()
g.display()
g.play(0, 'E')
g.display()
g.play(1, 'c')
g.display()
g.play(0, 'D')
g.display()
g.play(1, 'a')
g.display()
