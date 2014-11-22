from PyQt5.QtWidgets import QApplication
import logging
from awale.gui.simulator import SimulatorWindow


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Run app  ")
    a = QApplication([])
    w = SimulatorWindow()
    w.show()
    a.exec_()
