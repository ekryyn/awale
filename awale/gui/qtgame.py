import sys
from PyQt4 import QtGui, uic
from ui_qtgame import Ui_MainWindow


def draw_game(game, scene):
    scene.addRect(0,0, 20,10)

class GameWindow(QtGui.QMainWindow):
    def __init__(self):
        super(GameWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        scene = QtGui.QGraphicsScene()
        self.ui.game_view.setScene(scene)
        draw_game([1,2,3,4], self.ui.game_view.scene())
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = GameWindow()
    sys.exit(app.exec_())
