from itertools import cycle
import subprocess
from awale.core import GameState, can_play, winner


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

    running = True

    def run(self):
        game = GameState()

        players = [
            Player(0, create_process()),
            Player(1, create_process())
        ]

        p_cycle = cycle(players)

        while self.running:
            p = p_cycle.next()  # next player
            send_state(p.stdin, game)

            # print block_until_line(p.stdout)

            # wait for p's move
            ln = block_until_line(p.stdout)

            try:
                move = int(ln) - 1
            except ValueError:
                print("Error while processing move for player %d" % p.pid)
                print("Exit.")
                self.running = False
            else:
                # play it
                game.play(p.pid, LETTERS[move])

            if game.over():
                print("Finished, winner: %s" % winner(game.scores))
                self.running = False

        # kill sub processes
        for p in players:
            p.process.terminate()

if __name__ == '__main__':
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        app.running = False
        print("Shutting down...")
