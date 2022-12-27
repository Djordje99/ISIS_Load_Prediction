from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from services.scorer.ploting import CustomPloting
from gui.thread.saver_thread import SavingThread
from gui.thread.training_thread import TrainingThread
from gui.thread.predict_thread import PredictThread
from gui.thread.table_thread import TableThread



class LoadPredictionController(QMainWindow):
    def __init__(self):
        super(LoadPredictionController, self).__init__()

        uic.loadUi('gui\load_prediction_xml.ui', self)
        self.__connect_buttons()
        self.show()

        self.csv_path = ''

        #self.init_training()


    def __connect_buttons(self):
        self.csv_btn.clicked.connect(self.load_csv)
        self.save_csv_btn.clicked.connect(self.save_csv)
        self.train_btn.clicked.connect(self.init_training)
        self.predict_btn.clicked.connect(self.predict)


    def predict(self):
        date_form_predict = self.predict_date.dateTime()
        date_from = date_form_predict.toString('yyyy-MM-dd')

        day_number = self.predict_days_num.value()
        date_to_predict = date_form_predict.addDays(day_number)
        date_to = date_to_predict.toString('yyyy-MM-dd')

        self.saver_thread = PredictThread(date_from, date_to)

        # self.saver_thread.finish_signal.connect(self.saver_thread.deleteLater)
        self.saver_thread.finished.connect(self.saver_thread.deleteLater)
        self.saver_thread.finish_signal.connect(self.data_predicted)

        self.saver_thread.start()


    def data_predicted(self):
        QMessageBox.information(self, "Info", 'Prediction Done', QMessageBox.Ok)
        self.table_thread = TableThread(self.table)
        self.table_thread.finished.connect(self.table_thread.deleteLater)
        self.table_thread.start()



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
        self.saver_thread = SavingThread(self.csv_path)

        # self.saver_thread.finish_signal.connect(self.saver_thread.deleteLater)
        self.saver_thread.finished.connect(self.saver_thread.deleteLater)
        self.saver_thread.finish_signal.connect(self.data_saved)

        self.saver_thread.start()

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
        # date_form = self.from_date_edit.dateTime()
        # date_to = self.to_date_edit.dateTime()

        # if date_to <= date_form:
        #     QMessageBox.critical(self, "Error", 'Invalid dates input', QMessageBox.Ok)
        #     return

        self.training_thread = TrainingThread()

        # self.training_thread.finish_signal.connect(self.training_thread.deleteLater)
        self.training_thread.finished.connect(self.training_thread.deleteLater)
        self.training_thread.finish_signal.connect(self.training_finished)

        self.training_thread.start()



    def training_finished(self, y_predicted, y_test):
        self.ploting = CustomPloting()

        # self.widget.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # self.setCentralWidget(self.widget)

        # self.show()
        self.ploting.show_plots(y_predicted, y_test)

        QMessageBox.information(self, "Info", 'Training is finished', QMessageBox.Ok)
