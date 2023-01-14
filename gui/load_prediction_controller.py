from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from database.controller import DatabaseController

from services.scorer.ploting import CustomPloting
from gui.thread.saver_thread import SavingThread
from gui.thread.training_thread import TrainingThread
from gui.thread.predict_thread import PredictThread
from gui.thread.table_thread import TableThread
from services.exporter.csv import CsvExporter

from gui.tabs.predicted_load_tab import PredictedLoadTab
from gui.tabs.coal_generator_tab.coal_generator_tab import CoalGeneratorTab
from gui.tabs.gas_generator_tab.gas_generator_tab import GasGeneratorTab
from gui.tabs.hydro_generator_tab import HydroGeneratorTab
from gui.tabs.wind_generator_tab.wind_generator_tab import WindGeneratorTab
from gui.tabs.solar_generator_tab.solar_generator_tab import SolarGeneratorTab
from gui.tabs.optimize_tab import OptimizeTab

from load_optimization.service.optimizator.simplex.calculator import Calculator

SQLITE_MODE = ['append', 'replace']


class LoadPredictionController(QMainWindow):
    def __init__(self):
        super(LoadPredictionController, self).__init__()

        uic.loadUi('gui\load_prediction_xml.ui', self)
        self.__connect_buttons()
        self.show()

        self.database_controller = DatabaseController()

        self.training_folder_path = ''
        self.test_csv_path = ''

        self.predict_tab = PredictedLoadTab(self.predicted_load)
        self.optimize_tab = OptimizeTab(self.optimization)
        self.coal_generator_tab = CoalGeneratorTab(self.coal)
        self.gas_generator_tab = GasGeneratorTab(self.gas)
        self.hydro_generator_tab = HydroGeneratorTab(self.hydro)
        self.wind_generator_tab = WindGeneratorTab(self.wind)
        self.solar_generator_tab = SolarGeneratorTab(self.solar)

        self.sqlite_mode.addItems(SQLITE_MODE)
        #self.init_training()


    def __connect_buttons(self):
        self.csv_btn.clicked.connect(self.load_training_data)
        self.save_csv_btn.clicked.connect(self.save_training_data)
        self.train_btn.clicked.connect(self.init_training)
        self.predict_btn.clicked.connect(self.predict)
        self.export_btn.clicked.connect(self.export_csv)
        self.load_test_btn.clicked.connect(self.load_test_data)
        self.save_test_btn.clicked.connect(self.save_test_data)
        self.optimize_btn.clicked.connect(self.optimize)


    def optimize(self):
        coal_generator = self.coal_generator_tab.get_coal_generator_model()
        gas_generator = self.gas_generator_tab.get_gas_generator_model()
        hydro_generator = self.hydro_generator_tab.get_hydro_generator_model()
        solar_generator = self.solar_generator_tab.get_solar_generator_model()
        wind_generator = self.wind_generator_tab.get_wind_generator_model()

        cost_weight = self.optimize_tab.get_cost_weight_factor()
        co2_weight = self.optimize_tab.get_co2_weight_factor()

        calculator = Calculator(coal_generator, gas_generator, hydro_generator, solar_generator, wind_generator, cost_weight, co2_weight)

        result = calculator.call_simplex()

        self.optimize_tab.update_table(result)


    def load_test_data(self):
        self.test_csv_path, _ = QFileDialog.getOpenFileName(self, "Select CSV file", "C:\'","CSV Files (*.csv);;All Files (*)")
        self.load_test_line_edit.setText(self.test_csv_path)

        if self.test_csv_path != '':
            self.save_test_btn.setEnabled(True)
        else:
            self.save_test_btn.setEnabled(False)


    def save_test_data(self):
        self.database_controller.save_test_data(self.test_csv_path)

        QMessageBox.information(self, "Info", 'Test data is saved in database', QMessageBox.Ok)


    def load_training_data(self):
        self.training_folder_path = QFileDialog.getExistingDirectory(self,'Select a directory','C:\'' if self.training_folder_path == "" else self.training_folder_path)
        self.csv_line_edit.setText(self.training_folder_path)

        if self.training_folder_path != '':
            self.save_csv_btn.setEnabled(True)
            self.mode = self.sqlite_mode.currentText()
        else:
            self.save_csv_btn.setEnabled(False)
            self.from_date_edit.setEnabled(False)
            self.to_date_edit.setEnabled(False)
            self.train_btn.setEnabled(False)


    def save_training_data(self):
        self.saver_thread = SavingThread(self.training_folder_path, self.sqlite_mode.currentText())
        self.saver_thread.finished.connect(self.saver_thread.deleteLater)
        self.saver_thread.finish_signal.connect(self.data_saved)

        self.saver_thread.start()


    def data_saved(self, max_date, min_date):
        QMessageBox.information(self, "Info", 'Data is saved in database', QMessageBox.Ok)

        self.__set_dates(max_date, min_date)


    def __set_dates(self, max_date, min_date):
        print(max_date)
        q_date_min = QDateTime.fromString(min_date, 'yyyy-MM-dd hh:mm:ss')
        q_date_max = QDateTime.fromString(max_date, 'yyyy-MM-dd hh:mm:ss')

        print(q_date_max)

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

        date_form = date_form.toString('yyyy-MM-dd')
        date_to = date_to.toString('yyyy-MM-dd')

        self.training_thread = TrainingThread(date_form, date_to)

        self.training_thread.finished.connect(self.training_thread.deleteLater)
        self.training_thread.finish_signal.connect(self.training_finished)

        self.training_thread.start()


    def training_finished(self, y_predicted, y_test):
        self.ploting = CustomPloting()

        self.ploting.show_plots(y_predicted, y_test)

        QMessageBox.information(self, "Info", 'Training is finished', QMessageBox.Ok)


    def predict(self):
        date_form_predict = self.predict_date.dateTime()
        date_from = date_form_predict.toString('yyyy-MM-dd')

        day_number = self.predict_days_num.value()
        date_to_predict = date_form_predict.addDays(day_number)
        date_to = date_to_predict.toString('yyyy-MM-dd')

        self.saver_thread = PredictThread(date_from, date_to, day_number)
        self.saver_thread.finished.connect(self.saver_thread.deleteLater)
        self.saver_thread.finish_signal.connect(self.data_predicted)

        self.saver_thread.start()


    def data_predicted(self):
        QMessageBox.information(self, "Info", 'Prediction Done', QMessageBox.Ok)
        self.table_thread = TableThread(self.table)
        self.table_thread.finished.connect(self.table_thread.deleteLater)

        self.table_thread.start()

        self.predict_tab.refresh_graph()


    def export_csv(self):
        exporter = CsvExporter()
        exporter.export()
