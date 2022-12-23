from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from gui.load_prediction_controller import LoadPredictionController
from optimizer.genetic_feature_selection import GeneticFeatureSelection
from database.controller import DatabaseController


if __name__ == '__main__':
    # db_controller = DatabaseController()
    # data_frame = db_controller.load_data()
    # column_num = len(data_frame.columns)

    # gen_optimizer = GeneticFeatureSelection()

    # population = gen_optimizer.run_genetic_selection(column_num, data_frame, 5)

    # print(population)

    app = QApplication(sys.argv)
    main_window = LoadPredictionController()
    app.exec_()
