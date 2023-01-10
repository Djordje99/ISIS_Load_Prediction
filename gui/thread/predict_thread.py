from PyQt5.QtCore import QThread, pyqtSignal
from services.predictor.predict_load import LoadPredictor
import debugpy

class PredictThread(QThread):
    finish_signal = pyqtSignal()

    def __init__(self, date_from, date_to, day_number):
        super(PredictThread, self).__init__()
        self.predictor = LoadPredictor()
        self.date_from = date_from
        self.date_to = date_to
        self.day_number = day_number


    def run(self):
        debugpy.debug_this_thread()
        self.predictor.predict_test_data(self.date_from, self.date_to, self.day_number)
        self.finish_signal.emit()