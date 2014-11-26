from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty
from awale import core


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
