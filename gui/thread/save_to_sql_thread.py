from PyQt5.QtCore import QThread, pyqtSignal

from database.controller import DatabaseController

class SaveToSqlThread(QThread):
    finish_signal = pyqtSignal()


    def __init__(self, path):
        super().__init__()
        self.database_controller = DatabaseController()
        self.path = path

    def run(self):
        self.database_controller.save_to_db(self.path)
        self.finish_signal.emit()