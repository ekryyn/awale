def display_cell(c):
    return "[%2d]" % c


def display_game(game, scores):
    half = int(len(game)/2)
    p0_line = game[:half]
    p1_line = reversed(game[half:])
    o = ''
    o += ("                      %s\n" % "   ".join('abcdef'))
    o += ("                |  %s  | <- Model 2 (%2d)\n" % ("".join(map(display_cell, p1_line)), scores[1]))
    o += ("(%2d) Model 1 -> |  %s  |\n" % (scores[0], "".join(map(display_cell, p0_line))))
    o += ("                      %s\n" % "   ".join('ABCDEF'))
    return o


class Console(object):
    def process_message(self, msg_type, msg_val):
        if msg_type == 'game_state':
            g = display_game(msg_val['game'], msg_val['scores'])
            print(g)
        else:
            print(msg_val)
