import sqlite3
import pandas as pd

from services.preprocessing.weather.temperature_calibrator import TemperatureCalibrator
from services.preprocessing.weather.weather_calibrator import WeatherCalibrator

from services.preprocessing.data_combiner import DataCombiner

from services.preprocessing.normalizer.date import DateNormalizer
from services.preprocessing.normalizer.missing_value import MissingValue
from services.preprocessing.normalizer.string import StringNormalizer

DATABASE_NAME = 'database/load_database.db'


class DatabaseController():
    def __init__(self):
        self.calibrator = TemperatureCalibrator()
        self.weather_calibrator = WeatherCalibrator()


    def save_to_db(self, folder_path):
        self.data_combiner = DataCombiner(folder_path)
        self.data_frame = self.data_combiner.generate_training_data()

        self.data_frame = self.weather_calibrator.drop_features(data_frame=self.data_frame)
        self.data_frame = self.calibrator.fill_missing_value(data_frame=self.data_frame)
        self.data_frame = self.calibrator.fill_mean_temperature(data_frame=self.data_frame)
        self.data_frame = self.weather_calibrator.interpolate_missing_value(data_frame=self.data_frame)

        self.date_normalizer = DateNormalizer(self.data_frame)
        self.data_frame = self.date_normalizer.normalize_date()

        self.string_normalizer = StringNormalizer(self.data_frame)
        self.data_frame = self.string_normalizer.normalize_string()

        self.missing_value_normalizer = MissingValue(self.data_frame)
        self.data_frame = self.missing_value_normalizer.normalize_missing_value()

        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists='replace')
        self.connection.close()


    def get_max_min_dates(self):
        return self.data_frame['date'].max(), self.data_frame['date'].min()


    def get_data_frame(self):
        return self.data_frame


    def load_data(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%d %H:%M:%S')

        self.data_frame = self.weather_calibrator.drop_features(data_frame=self.data_frame)

        self.date_normalizer = DateNormalizer(self.data_frame)
        self.data_frame = self.date_normalizer.normalize_date()

        self.string_normalizer = StringNormalizer(self.data_frame)
        self.data_frame = self.string_normalizer.normalize_string()

        self.missing_value_normalizer = MissingValue(self.data_frame)
        self.data_frame = self.missing_value_normalizer.normalize_missing_value()

        return self.data_frame