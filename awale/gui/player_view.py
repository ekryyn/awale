from awale.gui.ui_player_view import Ui_Form
from PyQt5.QtWidgets import QWidget, QFileDialog


class PlayerView(QWidget):

    victories, defeats, draws = 0, 0, 0

    def __init__(self, parent):
        super(PlayerView, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.player_cmd.setText("python2 run_ia.py")

        self.ui.browse_btn.clicked.connect(self.update_cmd_path)

    @property
    def player_cmd(self):
        return self.ui.player_cmd.text()

    def update_cmd_path(self):
        path = QFileDialog.getOpenFileName()[0]
        self.ui.player_cmd.setText(path)

    def set_name(self, name):
        self.ui.groupBox.setTitle(name)

    def update_player_stats(self, player):
        self.ui.victories.setText(str(player.victories))
        self.ui.draws.setText(str(player.draws))
        self.ui.defeats.setText(str(player.defeats))
        self.ui.moves_played.setText(str(round(player.moves_played_per_game, 2)))
        self.ui.valid_moves_mean.setText(str(round(player.valid_moves_mean, 2)))
        self.ui.time_per_turn.setText(str(round(player.time_per_turn, 5)))

        self.ui.win_percent.setText(
            "%s%%" % round(player.win_percent, 2)
        )

