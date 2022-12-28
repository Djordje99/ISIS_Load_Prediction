from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from database.controller import DatabaseController
import debugpy

class SavingThread(QThread):
    finish_signal = pyqtSignal(str, str)

    def __init__(self, path, mode):
        super(SavingThread, self).__init__()
        self.database_controller = DatabaseController()
        self.path = path
        self.mode = mode


    def run(self):
        debugpy.debug_this_thread()
        self.database_controller.save_to_db(self.path, self.mode)
        max_date, min_date = self.database_controller.get_max_min_dates()
        self.finish_signal.emit(max_date, min_date)