# coding: utf-8
from itertools import cycle, islice, takewhile
from functools import partial

def player_id(game, index):
    """ _index_ belongs to player 0 or 1 """
    l = len(game)/2
    return 0 if index < l else 1

def can_play(game, player, index):
    """ _player_ can play on _index_ """
    return player == player_id(game, index)

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
        print(i)
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

game = [4] * 12
scores = [0, 0]
display_game(game, scores)
