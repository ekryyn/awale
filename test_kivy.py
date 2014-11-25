from pygame import time
import threading
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, BooleanProperty, AliasProperty, \
    ListProperty, ObjectProperty, ReferenceListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
import subprocess
from awale import core
from awale.gui.console import display_game
import time


class PlayerLine(BoxLayout):
    pass


class GameState(EventDispatcher):
    game = ListProperty([4]*12)
    scores = ListProperty([0, 0])
    current_player = NumericProperty(0)

    state = ReferenceListProperty(game, scores, current_player)

    def over(self):
        return core.game_over(self.game, self.scores, self.current_player)

    def current_player_can_play(self, index):
        return core.can_play(self.game,
                             self.scores,
                             self.current_player,
                             index)[0]

    def play_index(self, index):
        if not self.current_player_can_play(index):
            raise core.WrongMove("You can't play this !")

        # play
        self.game, self.scores, self.current_player = core.next_state(
            self.game, self.scores, self.current_player, index
        )


class DisplayGameState(GameState):
    def __init__(self, game_state, **kwargs):
        super(DisplayGameState, self).__init__(**kwargs)
        self.game_state = game_state
        self.game_state.bind(state=self.update_state)

    def update_state(self, *args):
        pass
        # self.state = self.game_state.state


class Hole(Widget):
    SIZE = 80
    amount = NumericProperty(None)
    hovered = BooleanProperty(False)
    highlighted = BooleanProperty(False)

    def __init__(self, index, **kwargs):
        super(Hole, self).__init__(**kwargs)
        self.index = index

    def get_color(self):
        if self.hovered:
            if self.parent and self.parent.hole_can_be_played_by_human(self):
                return .2, .6, .2
            else:
                return .6, .2, .2
        elif self.highlighted:
            return .2, .2, .6
        else:
            return .2, .2, .2

    def set_color(self, value):
        pass

    color = AliasProperty(get_color, set_color, bind=('hovered', 'highlighted',))


def get_hole_offset(game, index):
    pid = core.player_id(game, index)
    y = -Hole.SIZE + pid*Hole.SIZE

    center_x_off = len(game)*Hole.SIZE/4

    if pid == 0:
        x = Hole.SIZE*index - center_x_off
    else:
        x = ((len(game)-1) - index) * Hole.SIZE - center_x_off

    return x, y


class Board(Widget):
    hovered_hole = ObjectProperty(None, allownone=True)
    game_state = ObjectProperty(None)
    game_to_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.humans = [0, ]

        self.bind(size=self.draw_board)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.game_state = GameState()
        self.game_to_display = DisplayGameState(self.game_state)
        self.game_to_display.bind(state=self.draw_board)

        self.register_event_type('on_player_move')

    def hole_can_be_played_by_human(self, hole):
        if self.game_state.current_player not in self.humans:
            return False
        return self.game_state.current_player_can_play(hole.index)

    def on_mouse_pos(self, instance, pos):
        child = None
        for c in self.children:
            inside = c.collide_point(*pos)
            if inside:
                child = c

        # we're on child :
        if child:
            if self.hovered_hole != child:
                if self.hovered_hole:
                    self.hovered_hole.hovered = False
                self.hovered_hole = child
                child.hovered = True
        else:
            if self.hovered_hole:
                self.hovered_hole.hovered = False
            self.hovered_hole = None

    def on_touch_down(self, touch):
        """
        Triggered when clicked
        """
        if self.hovered_hole:
            if self.hole_can_be_played_by_human(self.hovered_hole):
                self.play_move(self.hovered_hole.index)

    def on_hovered_hole(self, instance, hole):
        self.highlight_next(hole)
        if hole is not None and self.hole_can_be_played_by_human(hole):
            # I choose not to take the full next state,
            # but just before eating instead
            game, last = core.step_game(self.game_state.game, hole.index)
            ns = core.next_state(self.game_state.game,
                                 self.game_state.scores,
                                 self.game_state.current_player,
                                 hole.index)
            self.game_to_display.state = (
                game,
                self.game_state.scores,
                core.other_player(self.game_state.current_player)
            )
        else:
            self.game_to_display.state = self.game_state.state

    def play_move(self, index):
        self.game_state.play_index(index)
        print(
            display_game(self.game_state.game, self.game_state.scores)
        )
        # remove all highlighting
        for h in self.children:
            h.highlighted = False
            h.hovered = False

        # dispatch event
        self.dispatch('on_player_move')

    def draw_board(self, *args):
        self.clear_widgets()
        for i, a in enumerate(self.game_to_display.game):
            off_x, off_y = get_hole_offset(self.game_state.game, i)
            x = self.center_x + off_x
            y = self.center_y + off_y
            h = Hole(i, amount=a, pos=(x, y))
            self.add_widget(h.__self__)

    def highlight_next(self, hole):
        if hole:
            a = self.game_state.game[hole.index]
            indexes = list(range(len(self.game_state.game)))
            indexes = core.rotate(indexes, -hole.index)[1:a+1]
            valid_hole = self.hole_can_be_played_by_human(hole)

            if valid_hole:
                for h in self.children:
                    h.highlighted = h.index in indexes
                return

        for h in self.children:
            h.highlighted = False

    def on_player_move(self):
        pass

    def current_is_human(self):
        return self.game_state.current_player in self.humans


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.register_event_type('on_ai_to_play')
        self.ids.board.bind(on_player_move=self.on_player_move)

    def process_ai_move(self, move):
        self.ids.board.play_move(move)

    def on_player_move(self, instance):
        if not self.ids.board.current_is_human():
            self.dispatch('on_ai_to_play')

    def get_game_state(self):
        return self.ids.board.game_state.state

    def on_ai_to_play(self):
        pass


class AIRunner(threading.Thread):
    def __init__(self, listener):
        super(AIRunner, self).__init__()
        self.listener = listener
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
                self.listener.process_ai_move(move)

                # fall asleep
                self.sleeping = True

            time.sleep(.001)

        # exiting
        if self.process:
            self.process.terminate()

    def ask_for_play(self, game, scores, player):
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


class AwaleApp(App):
    ai_runner = None

    def build(self):
        # print("building")
        w = MainWindow()
        w.bind(on_ai_to_play=self.on_ai_to_play)
        self.ai_runner = AIRunner(w)  # set board as listener

        return w

    def on_ai_to_play(self, instance):
        self.ai_runner.ask_for_play(*instance.get_game_state())

    def on_start(self):
        # print("starting")
        self.ai_runner.start()

    def on_stop(self):
        # print("exiting")
        self.ai_runner.stop()
        self.ai_runner.join()

if __name__ == "__main__":
    AwaleApp().run()
