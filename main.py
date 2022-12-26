from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from gui.load_prediction_controller import LoadPredictionController


if __name__ == '__main__':
    # gen_optimizer = GeneticFeatureSelection()
    # population = gen_optimizer.run_genetic_selection(64, 100)
    # print(population)

    app = QApplication(sys.argv)
    main_window = LoadPredictionController()
    app.exec_()
