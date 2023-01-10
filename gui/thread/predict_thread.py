from PyQt5.QtCore import QThread, pyqtSignal
from services.predictor.predict_load import LoadPredictor
from datetime import datetime
import debugpy

DATE_TRAINING = '2021-09-06'

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

        start_predict = datetime.strptime(self.date_from, "%Y-%m-%d")
        limit = datetime.strptime(DATE_TRAINING, "%Y-%m-%d")

        if start_predict < limit:
            self.predictor.predict(self.date_from, self.date_to, self.day_number)
        else:
            self.predictor.predict_test_data(self.date_from, self.date_to, self.day_number)

        self.finish_signal.emit()