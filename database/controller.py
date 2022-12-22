import sqlite3
import pandas as pd
import os

from services.preprocessing.weather.temperature_calibrator import TemperatureCalibrator
from services.preprocessing.weather.weather_calibrator import WeatherCalibrator

from services.preprocessing.data_combiner import DataCombiner


# LOAD_PATH = '\NYS_Load_Data'
# WEATHER_PATH = '\NYS_Weather_Data\New_York_City_NY'

DATABASE_NAME = 'database/load_database.db'

class DatabaseController():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.calibrator = TemperatureCalibrator()
        self.weather_calibrator = WeatherCalibrator()


    def save_to_db(self):
        # self.load_loader = LoadDataLoader(f'{csv_path}{LOAD_PATH}')
        # self.weather_loader = WeatherDataLoader(f'{csv_path}{WEATHER_PATH}')
        self.data_frame = self.load_data_frame()

        self.data_frame = self.calibrator.fill_missing_value(data_frame=self.data_frame)
        self.data_frame = self.calibrator.fill_mean_temperature(data_frame=self.data_frame)
        self.data_frame = self.weather_calibrator.interpolate_missing_value(data_frame=self.data_frame)

        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists='replace')
        self.connection.close()


    def get_max_min_dates(self):
        return self.data_frame['date'].max(), self.data_frame['date'].min()


    def get_data_frame(self):
        return self.data_frame


    def load_data_frame(self):
        self.data_combiner = DataCombiner(self.folder_path)
        return self.data_combiner.generate_training_data()


        # self.connection = sqlite3.connect(DATABASE_NAME)
        # self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        # self.connection.close()

        # self.data_frame = self.data_frame.drop(['index'], axis=1)

        # self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%d %H:%M:%S')

        # return self.data_frame