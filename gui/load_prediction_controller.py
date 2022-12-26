from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from services.training.model_creator import ModelCreator
from services.predictor.predict_load import LoadPredictor

from gui.thread.save_to_sql_thread import SaveToSqlThread

class LoadPredictionController(QMainWindow):
    def __init__(self):
        super(LoadPredictionController, self).__init__()

        uic.loadUi('gui\load_prediction_xml.ui', self)
        self.__connect_buttons()
        self.show()

        self.csv_path = ''

        self.init_training()


    def __connect_buttons(self):
        self.csv_btn.clicked.connect(self.load_csv)
        self.save_csv_btn.clicked.connect(self.save_csv)
        self.train_btn.clicked.connect(self.init_training)
        self.predict_btn.clicked.connect(self.predict)


    def predict(self):
        self.predictor = LoadPredictor()

        date_form_predict = self.predict_date.dateTime()
        date_from = date_form_predict.toString('yyyy-MM-dd')

        day_number = self.predict_days_num.value()
        date_to_predict = date_form_predict.addDays(day_number)
        date_to = date_to_predict.toString('yyyy-MM-dd')

        self.predictor.predict(date_from, date_to)


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
        self.thread = SaveToSqlThread()
        self.thread.progress_signal.connect(self.data_saved)
        self.thread.start()

    def data_saved(self):
        QMessageBox.information(self, "Info", 'Data is saved in database', QMessageBox.Ok)

        self.__set_dates()


    def __set_dates(self):
        max_date, min_date = self.database_controller.get_max_min_dates()

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
        self.model_creator = ModelCreator()

        # date_form = self.from_date_edit.dateTime()
        # date_to = self.to_date_edit.dateTime()

        # if date_to <= date_form:
        #     QMessageBox.critical(self, "Error", 'Invalid dates input', QMessageBox.Ok)
        #     return

        self.model_creator.create_model()

        QMessageBox.information(self, "Info", 'Training is finished', QMessageBox.Ok)
