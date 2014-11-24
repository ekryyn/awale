from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty, AliasProperty, \
    ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from awale.core import player_id, can_play, rotate, GameState
from awale.gui.console import display_game


class PlayerLine(BoxLayout):
    pass


class Hole(Widget):
    SIZE = 80
    amount = NumericProperty(8)
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

    def get_display_amount(self):
        if self.highlighted:
            return self.amount + 1
        elif self.hovered and self.parent.hole_can_be_played(self):
            return 0
        return self.amount

    def set_display_amount(self, value):
        pass

    color = AliasProperty(get_color, set_color, bind=('hovered', 'highlighted',))
    display_amount = AliasProperty(
        get_display_amount,
        set_display_amount,
        bind=('hovered', 'highlighted', 'amount')
    )


def get_hole_offset(game, index):
    pid = player_id(game, index)
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
    scores = ListProperty(None)

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.game_state = GameState()
        self.bind(size=self.draw_board)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.register_event_type('on_game_state_changed')

        self.scores = self.game_state.scores

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
        if self.hovered_hole:
            if self.hole_can_be_played(self.hovered_hole):
                self.game_state.play_index(self.hovered_hole.index)
                self.dispatch('on_game_state_changed')
                print(
                    display_game(self.game_state.game, self.game_state.scores)
                )

    def on_hovered_hole(self, instance, hole):
        self.highlight_next(hole)

    def draw_board(self, *args):
        self.clear_widgets()
        for i, a in enumerate(self.game_state.game):
            off_x, off_y = get_hole_offset(self.game_state.game, i)
            x = self.center_x + off_x
            y = self.center_y + off_y
            h = Hole(i, amount=a, pos=(x, y))
            self.add_widget(h.__self__)

        print("Ch: %d" % len(self.children))

    def highlight_next(self, hole):
        if hole:
            a = self.game_state.game[hole.index]
            indexes = list(range(len(self.game_state.game)))
            indexes = rotate(indexes, -hole.index)[1:a+1]
            valid_hole = self.hole_can_be_played(hole)

            if valid_hole:
                for h in self.children:
                    h.highlighted = h.index in indexes
                return

        for h in self.children:
            h.highlighted = False

    def on_game_state_changed(self):
        self.draw_board()
        self.scores = self.game_state.scores


class MainWindow(BoxLayout):
    pass


class AwaleApp(App):
    def build(self):
        w = MainWindow()
        return w


    def toto(self):
        print('clicked')

if __name__ == "__main__":
    AwaleApp().run()
