import subprocess
import threading
import time
from awale import core


class HumanPlayer(object):
    """
    This class listens for a move request make the necessary to play a move
    """
    def __init__(self, board):
        self.board = board

    def on_move_required(self, game, scores, player):
        pass


class AIPlayer(threading.Thread):
    def __init__(self, board):
        super(AIPlayer, self).__init__()
        self.board = board
        self.process = None
        self.running = False
        self.sleeping = True

    def stop(self):
        self.running = False

    def run(self):
        cmd = "python run_ia.py"
        self.process = subprocess.Popen(
            cmd.split(' '),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            close_fds=True,
            universal_newlines=True,
            bufsize=0,
        )
        self.running = True
        while self.running:
            if not self.sleeping:
                # when woke up, fetch the move
                ln = ''
                while not ln:
                    ln = self.process.stdout.readline()
                move = int(ln.strip()) - 1

                # notify listener
                self.board.play_move(move)

                # fall asleep
                self.sleeping = True

            time.sleep(.001)

        # exiting
        if self.process:
            self.process.terminate()

    def on_move_required(self, game, scores, player):
        """
        Ask the runner to get the next move.
        The runner will notify the listener when it's done.
        Return True if the request has been taken in account.
        Return False if the runner can't satisfy the request for now.
        """
        if not self.sleeping:
            # busy, don't do anything
            return False

        game_ = ' '.join(str(a) for a in game)
        scores_ = ' '.join(str(s) for s in scores)
        to_play = str(player + 1)
        vms = [
            str(i+1)
            for i, s in core.next_valid_states(game, scores, player)
        ]
        valid_moves = ' '.join(vms)
        lines = "%s\n%s\n%s\n%s\n" % (
            game_,
            scores_,
            to_play,
            valid_moves,
        )
        self.process.stdin.write(lines)

        # awake, so we'll fetch the next move soon
        self.sleeping = False
        return True
