from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from awale import core
from awale.gui.console import display_game
from awale.gui.kvgame.game_state import GameState, DisplayGameState
from awale.gui.kvgame.hole import Hole


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
        self.player_listeners = []

        self.bind(size=self.draw_board)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.game_state = GameState()
        self.game_to_display = DisplayGameState(self.game_state)
        self.game_to_display.bind(state=self.draw_board)

        self.register_event_type('on_player_move')

    def add_player_listener(self, pl):
        self.player_listeners.append(pl)

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
