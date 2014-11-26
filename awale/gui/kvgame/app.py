from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from awale.gui.kvgame.player_logic import AIPlayer
from awale.gui.kvgame.board import Board as _Board


# to prevent unused import :D
Board = _Board


class PlayerLine(BoxLayout):
    pass


class MainWindow(BoxLayout):
    pass


class AwaleApp(App):
    ai_runner = None

    def build(self):
        # print("building")
        w = MainWindow()
        self.ai_runner = AIPlayer(w.ids.board)

        return w

    def on_start(self):
        # print("starting")
        self.ai_runner.start()

    def on_stop(self):
        # print("exiting")
        self.ai_runner.stop()
        self.ai_runner.join()



