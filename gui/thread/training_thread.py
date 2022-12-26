from PyQt5.QtCore import QThread, pyqtSignal

from services.training.model_creator import ModelCreator
from services.scorer.ploting import CustomPloting


class TrainingThread(QThread):
    finish_signal = pyqtSignal()

    def run(self):
        self.creator = ModelCreator()
        custom_plotting = CustomPloting()

        y_predicted, y_test = self.creator.create_model()

        # custom_plotting.show_plots(y_predicted, y_test)

        self.finish_signal.emit()