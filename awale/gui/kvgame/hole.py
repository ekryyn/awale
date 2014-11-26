from kivy.properties import NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.widget import Widget


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

    color = AliasProperty(
        get_color,
        set_color,
        bind=('hovered', 'highlighted',)
    )
