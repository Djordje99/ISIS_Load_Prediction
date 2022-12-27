from PyQt5.QtCore import QThread, pyqtSignal
from services.predictor.predict_load import LoadPredictor

class PredictThread(QThread):
    finish_signal = pyqtSignal()

    def __init__(self, date_from, date_to):
        super(PredictThread, self).__init__()
        self.predictor = LoadPredictor()
        self.date_from = date_from
        self.date_to = date_to


    def run(self):
        self.predictor.predict(self.date_from, self.date_to)
        self.finish_signal.emit()