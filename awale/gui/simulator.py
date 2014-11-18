from awale.gui.ui_simulator import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from awale import ai_simulation


class SimulatorWindow(QMainWindow):
    def __init__(self):
        super(SimulatorWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app = None
        self.ui.player1.set_name('Player 1')
        self.ui.player2.set_name('Player 2')
        self.ui.nbGame.setValue(10)
        self.ui.nbGame.setMaximum(1000000)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setEnabled(False)

        self.ui.startButton.clicked.connect(self.run_simulation)

    def run_simulation(self):
        self.app = ai_simulation.App(
            self.ui.nbGame.value(),
            self.ui.player1.player_cmd,
            self.ui.player2.player_cmd,
            [self]
        )

        self.app.start()

    def closeEvent(self, event):
        if self.app:
            self.app.stop()
            self.app.join()

    def on_simulation_started(self):
        self.ui.progressBar.setRange(0, self.ui.nbGame.value())
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setEnabled(True)
        self.ui.startButton.setEnabled(False)

    def on_game_finished(self, player1, player2):
        self.ui.progressBar.setValue(
            self.ui.progressBar.value() + 1
        )
        self.ui.player1.update_player_stats(player1)
        self.ui.player2.update_player_stats(player2)

    def on_simulation_finished(self, chance_over_talent):
        self.app.stop()
        self.app = None
        self.ui.progressBar.setEnabled(False)
        self.ui.startButton.setEnabled(True)
        self.ui.reason.setText(
            "Chance" if chance_over_talent else "Talent"
        )
