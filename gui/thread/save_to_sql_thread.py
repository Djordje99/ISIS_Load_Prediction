import sys
from PyQt5.QtCore import QThread, pyqtSignal

from database.controller import DatabaseController

class SaveToSqlThread(QThread):
    finish_signal = pyqtSignal(int)

    def __init__(self) -> None:
        self.database_controller = DatabaseController()


    def run(self):
        self.database_controller.save_to_db(self.csv_path)
        self.finish_signal.emit()