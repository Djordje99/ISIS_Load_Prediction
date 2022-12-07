from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from gui.load_prediction_controller import LoadPredictionController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = LoadPredictionController()
    app.exec_()