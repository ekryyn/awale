from itertools import cycle
import subprocess
from awale.core import GameState, can_play, winner
from awale.gui.console import display_game


def block_until_line(stream):
    ln = ''
    while not ln:
        ln = stream.readline()
    return ln


def create_process():
    return subprocess.Popen(
        ["python2", "run_ia.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        close_fds=True
    )


class Player(object):
    """
    Simple player wrapper
    to store various information about him
    """
    def __init__(self, pid, process):
        self.pid = pid
        self.process = process
        self.victories = 0

    @property
    def stdout(self):
        return self.process.stdout

    @property
    def stdin(self):
        return self.process.stdin


def send_state(stdin, game):
    game_ = ' '.join(str(a) for a in game.game)
    scores_ = ' '.join(str(s) for s in game.scores)
    to_play = str(game.current_player + 1)
    valid_moves = ' '.join(
        str(i+1) for i, m in enumerate(game.game)
        if can_play(game.game, game.current_player, i)
    )
    lines = "%s\n%s\n%s\n%s\n" % (
        game_,
        scores_,
        to_play,
        valid_moves,
    )
    stdin.write(lines)


LETTERS = "ABCDEFfedcba"


class App(object):
    """
    Wrapper to easily kill subprocesses
    """

    running = False
    remaining_games = 0

    def stop(self):
        self.running = False
        self.remaining_games = 0

    def play_game(self, players):

        # initialize state
        game = GameState()
        p_cycle = cycle(players)
        over = False

        while self.running and not over:
            p = p_cycle.next()  # next player
            send_state(p.stdin, game)

            # wait for p's move
            ln = block_until_line(p.stdout)

            try:
                move = int(ln) - 1
            except ValueError:
                print("Error while processing move for player %d" % p.pid)
                print("Exit.")
                print("Last was:")
                print(display_game(last_game, last_scores))
                print("played %s" % move)
                self.stop()
            else:
                # play it
                last_game = game.game[:]
                last_scores = game.scores[:]
                game.play(p.pid, LETTERS[move])
                # print(display_game(game.game, game.scores))

            if game.over():
                # print("Finished, winner: %s" % winner(game.scores))
                win_id = winner(game.scores)
                if win_id is not None:
                    # not draw
                    p_winner = next(
                        p for p in players
                        if p.pid == win_id
                    )
                    p_winner.victories += 1
                over = True

    def run(self, number_of_games=1):

        self.running = True
        self.remaining_games = number_of_games

        players = [
            Player(0, create_process()),
            Player(1, create_process())
        ]

        while self.remaining_games > 0:
            self.play_game(players)
            self.remaining_games -= 1

        # scores
        for p in players:
            print("Player %d : %d victories." % (p.pid, p.victories))

        # import math
        # p = float(players[0].victories)/(players[0].victories+players[1].victories)
        # toto = abs(p - 0.5) > 2 * math.sqrt((p*(1-p))/(players[0].victories+players[1].victories))
        # print "Toto= %s" % toto

        # kill sub processes
        for p in players:
            p.process.terminate()

if __name__ == '__main__':
    app = App()
    try:
        app.run(1000)
    except KeyboardInterrupt:
        app.running = False
        print("Shutting down...")
