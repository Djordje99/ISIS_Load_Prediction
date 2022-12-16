from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from database.controller import DatabaseController
from services.preprocessing.load_preprocessed_data import LoadPreprocessedData
from services.preprocessing.weather.temperature_calibrator import TemperatureCalibrator

class LoadPredictionController(QMainWindow):
    def __init__(self):
        super(LoadPredictionController, self).__init__()

        uic.loadUi('gui\load_prediction_xml.ui', self)
        self.__connect_buttons()
        self.show()

        self.database_controller = DatabaseController()
        self.calibrator = TemperatureCalibrator()
        self.csv_path = ''


    def __connect_buttons(self):
        self.csv_btn.clicked.connect(self.load_csv)
        self.save_csv_btn.clicked.connect(self.save_csv)
        self.train_btn.clicked.connect(self.init_training)


    def load_csv(self):
        self.csv_path = QFileDialog.getExistingDirectory(self,'Select a directory','C:\'' if self.csv_path == "" else self.csv_path)
        self.csv_line_edit.setText(self.csv_path)

        if self.csv_path != '':
            self.save_csv_btn.setEnabled(True)
        else:
            self.save_csv_btn.setEnabled(False)
            self.from_date_edit.setEnabled(False)
            self.to_date_edit.setEnabled(False)

            self.train_btn.setEnabled(False)


    def save_csv(self):
        self.loader = LoadPreprocessedData(self.csv_path)
        self.data_frame = self.loader.load_data()

        data_frame = self.calibrator.fill_missing_value(data_frame=data_frame)

        self.database_controller.save_to_db(data_frame)

        QMessageBox.information(self, "Info", 'Data is saved in database', QMessageBox.Ok)

        self.__set_dates(data_frame['date'].min(), data_frame['date'].max())


    def __set_dates(self, min_date, max_date):
        q_date_min = QDateTime(min_date)
        q_date_max = QDateTime(max_date)

        self.from_date_edit.setMaximumDateTime(q_date_max)
        self.from_date_edit.setMinimumDateTime(q_date_min)

        self.to_date_edit.setMaximumDateTime(q_date_max)
        self.to_date_edit.setMinimumDateTime(q_date_min)

        self.from_date_edit.setEnabled(True)
        self.to_date_edit.setEnabled(True)

        self.train_btn.setEnabled(True)


    def init_training(self):
        date_form = self.from_date_edit.dateTime()
        date_to = self.to_date_edit.dateTime()

        if date_to <= date_form:
            QMessageBox.critical(self, "Error", 'Invalid dates input', QMessageBox.Ok)
            return

        
        #TODO train model between dates

        QMessageBox.information(self, "Info", 'Training is finished', QMessageBox.Ok)
