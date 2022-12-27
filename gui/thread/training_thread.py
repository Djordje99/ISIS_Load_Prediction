import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread

from services.training.model_creator import ModelCreator

class TrainingThread(QThread):
    finish_signal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        super(TrainingThread, self).__init__()


    def run(self):
        self.creator = ModelCreator()
        y_predicted, y_test = self.creator.create_model()

        self.finish_signal.emit(y_predicted, y_test)