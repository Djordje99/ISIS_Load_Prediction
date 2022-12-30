import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread

from services.training.model_creator import ModelCreator

class TrainingThread(QThread):
    finish_signal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, date_from, date_to):
        super(TrainingThread, self).__init__()
        self.date_from = date_from
        self.date_to = date_to


    def run(self):
        self.creator = ModelCreator()
        y_predicted, y_test = self.creator.create_model(self.date_from,  self.date_to)

        self.finish_signal.emit(y_predicted, y_test)