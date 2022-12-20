import sqlite3
import pandas as pd

from services.preprocessing.load_preprocessed_data import LoadPreprocessedData
from services.preprocessing.weather.temperature_calibrator import TemperatureCalibrator

DATABASE_NAME = 'database/load_database.sqlite'

class DatabaseController():
    def __init__(self):
        self.calibrator = TemperatureCalibrator()


    def save_to_db(self, csv_path):
        self.loader = LoadPreprocessedData(csv_path)
        self.data_frame = self.loader.load_data()

        self.data_frame = self.calibrator.fill_missing_value(data_frame=self.data_frame)
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists='replace')
        self.connection.close()


    def get_max_min_dates(self):
        return self.data_frame['date'].max(), self.data_frame['date'].min()


    def get_data_frame(self):
        return self.data_frame


    def load_data_frame(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%d %H:%M:%S')

        return self.data_frame