from itertools import cycle
import subprocess
from threading import Thread
from awale.core import valid_moves_indices
from core import GameState, winner
import time
from gui.console import display_game


def block_until_line(stream):
    ln = ''
    while not ln:
        ln = stream.readline()
    return ln


def create_process(cmd):
    return subprocess.Popen(
        cmd.split(' '),
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
        self.defeats = 0
        self.draws = 0
        self.moves_played = 0
        self.valid_moves_total = 0
        self.total_time = 0

    @property
    def valid_moves_mean(self):
        if self.moves_played:
            return float(self.valid_moves_total)/self.moves_played
        return 0.0

    @property
    def stdout(self):
        return self.process.stdout

    @property
    def stdin(self):
        return self.process.stdin

    @property
    def win_percent(self):
        try:
            return (
                100.0 * self.victories/self.games_played
            )
        except ZeroDivisionError:
            return 0.0

    @property
    def games_played(self):
        return self.victories + self.draws + self.defeats

    @property
    def moves_played_per_game(self):
        try:
            return float(self.moves_played)/self.games_played
        except ZeroDivisionError:
            return 0.0

    @property
    def time_per_turn(self):
        try:
            return float(self.total_time)/self.moves_played
        except ZeroDivisionError:
            return 0.0


def send_state(stdin, game):
    game_ = ' '.join(str(a) for a in game.game)
    scores_ = ' '.join(str(s) for s in game.scores)
    to_play = str(game.current_player + 1)
    valid_moves = ' '.join(
        str(i+1) for i in valid_moves_indices(game.game, game.current_player)
    )
    lines = "%s\n%s\n%s\n%s\n" % (
        game_,
        scores_,
        to_play,
        valid_moves,
    )
    stdin.write(lines)

    return valid_moves


LETTERS = "ABCDEFfedcba"


class App(Thread):
    """
    Wrapper to easily kill subprocesses
    """

    running = False
    remaining_games = 0

    def __init__(self, nb_games, cmd1, cmd2, listeners=None):
        super(App, self).__init__()
        self.remaining_games = nb_games
        self.listeners = listeners or []
        self.cmd1 = cmd1
        self.cmd2 = cmd2

    def notify_listeners(self, method_to_call, *args):
        for l in self.listeners:
            if hasattr(l, method_to_call):
                getattr(l, method_to_call)(*args)

    def stop(self):
        self.running = False
        self.remaining_games = 0
        self.notify_listeners('on_stop')

    def play_game(self, players):

        # initialize state
        game = GameState()
        p_cycle = cycle(players)
        over = False

        while self.running and not over:
            p = p_cycle.next()  # next player

            tm_before = time.time()
            send_state(p.stdin, game)
            # wait for p's move
            ln = block_until_line(p.stdout)
            tm_after = time.time()
            p.total_time += tm_after - tm_before

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
                # print(display_game(last_game, last_scores))
                last_game = game.game[:]
                last_scores = game.scores[:]
                game.play(p.pid, LETTERS[move])
                p.moves_played += 1
                p.valid_moves_total += len(
                    valid_moves_indices(game.game, game.current_player)
                )
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
                    p_loser = next(
                        p for p in players
                        if p.pid != win_id
                    )
                    p_winner.victories += 1
                    p_loser.defeats += 1
                else:
                    # draw
                    for p in players:
                        p.draws += 1
                over = True

    def run(self):

        self.running = True

        players = [
            Player(0, create_process(self.cmd1)),
            Player(1, create_process(self.cmd2))
        ]

        self.notify_listeners('on_simulation_started')

        while self.remaining_games > 0:
            self.play_game(players)
            self.remaining_games -= 1
            self.notify_listeners('on_game_finished', *players)

        # scores
        for p in players:
            print("Player %d : %d victories." % (p.pid, p.victories))

        import math
        p = float(players[0].victories)/(players[0].victories+players[1].victories)
        chance = abs(p - 0.5) > 2 * math.sqrt((p*(1-p))/(players[0].victories+players[1].victories))

        # kill sub processes
        for p in players:
            p.process.terminate()

        self.notify_listeners('on_simulation_finished', chance)

if __name__ == '__main__':
    app = App(
        1000,
        'python2 run_ia.py',
        # 'python2 run_ia.py',
        'awalecpp/benoit'
    )
    try:
        app.start()
        app.join()
    except KeyboardInterrupt:
        app.running = False
        print("Shutting down...")
        app.join()
