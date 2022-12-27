from PyQt5.QtCore import QThread, pyqtSignal
from database.controller import DatabaseController
from PyQt5.QtWidgets import QTableWidgetItem

class TableThread(QThread):
    def __init__(self, table):
        super(TableThread, self).__init__()
        self.controller = DatabaseController()
        self.table = table


    def run(self):
        data_frame = self.controller.load_predicted_load()

        self.table.setRowCount(data_frame.shape[0])
        self.table.setColumnCount(data_frame.shape[1])

        self.table.setHorizontalHeaderLabels(list(data_frame.columns))

        for i in range(data_frame.shape[0]):
            for j in range(data_frame.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(data_frame.iloc[i, j])))

        self.table.resizeColumnsToContents()
