from PyQt5.QtWidgets import QApplication
from awale.gui.simulator import SimulatorWindow


if __name__ == "__main__":
    a = QApplication([])
    w = SimulatorWindow()
    w.show()
    a.exec_()
