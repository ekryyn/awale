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
            if self.parent and self.parent.hole_can_be_played(self):
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
    x = Hole.SIZE*index
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
        self.bind(size=self.draw_board)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.game_state = GameState()
        self.game_to_display = GameState()
        self.game_to_display.bind(game=self.draw_board)
        self.game_to_display.bind(scores=self.draw_board)
        self.game_to_display.bind(current_player=self.draw_board)

    def hole_can_be_played(self, hole):
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
            if self.hole_can_be_played(self.hovered_hole):
                self.play_move(self.hovered_hole)

    def on_hovered_hole(self, instance, hole):
        self.highlight_next(hole)
        if hole is not None and self.hole_can_be_played(hole):
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

    def play_move(self, hole):
        self.game_state.play_index(hole.index)
        print(
            display_game(self.game_state.game, self.game_state.scores)
        )

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
            valid_hole = self.hole_can_be_played(hole)

            if valid_hole:
                for h in self.children:
                    h.highlighted = h.index in indexes
                return

        for h in self.children:
            h.highlighted = False


class MainWindow(BoxLayout):
    pass


class AIRunner(threading.Thread):
    def __init__(self, listener):
        super(AIRunner, self).__init__()

    def run(self):
        cmd = "python run_ia.py"
        process = subprocess.Popen(
            cmd.split(' '),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            close_fds=True,
            universal_newlines=True,
            bufsize=0,
        )


class AwaleApp(App):
    def build(self):
        w = MainWindow()
        return w

if __name__ == "__main__":
    AwaleApp().run()
