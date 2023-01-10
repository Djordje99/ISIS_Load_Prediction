import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem

from services.preprocessing.data_combiner import DataCombiner

DATABASE_NAME = 'database/load_database.db'


class DatabaseController():
    def get_data_frame(self):
        return self.load_data()


    def get_max_min_dates(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        self.connection.close()

        return self.data_frame['date'].max(), self.data_frame['date'].min()


    def save_training_data(self, folder_path, mode):
        self.data_combiner = DataCombiner(folder_path)

        self.raw_data_frame = self.data_combiner.generate_training_data()
        self.data_frame = self.data_combiner.preprocess_data(self.raw_data_frame)

        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists=mode)
        self.raw_data_frame.to_sql(name='RawLoad', con=self.connection, if_exists=mode)
        self.connection.close()


    def load_training_data(self, from_date = None, to_date = None):
        self.connection = sqlite3.connect(DATABASE_NAME)

        query = ''
        parameters = []

        if from_date == None or to_date == None:
            query = 'SELECT * FROM Load'
        else:
            query = 'SELECT * FROM Load WHERE date >= ? and date <= ?'
            parameters = [from_date, to_date]

        self.data_frame = pd.read_sql_query(query, params=parameters, con=self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


    def load_raw_training_data(self, from_date = None, to_date = None):
        self.connection = sqlite3.connect(DATABASE_NAME)

        query = ''
        parameters = []

        if from_date == None or to_date == None:
            query = 'SELECT * FROM RawLoad'
        else:
            query = 'SELECT * FROM RawLoad WHERE date >= ? and date <= ?'
            parameters = [from_date, to_date]

        self.data_frame = pd.read_sql_query(query, params=parameters, con=self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


    def save_predicted_load(self, y_predicted, date_from, day_number):
        date_from += ' 00:00:00'
        dates = pd.date_range(date_from, periods=day_number*24, freq='H')

        data_frame = pd.DataFrame({'date': dates, 'predicted_load': y_predicted.ravel()})

        data_frame = data_frame.set_index('date', drop=True)

        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame.to_sql(name='PredictedLoad', con=self.connection, if_exists='replace')
        self.connection.close()


    def load_predicted_load(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame = pd.read_sql_query('SELECT * FROM PredictedLoad', self.connection)
        self.connection.close()

        return data_frame


    def save_test_data(self, test_csv_path):
        data_frame = pd.read_csv(test_csv_path)

        data_frame = data_frame.rename(columns={'datetime': 'date'})
        data_frame['date'] = pd.to_datetime(data_frame['date'], format='%Y-%m-%dT%H:%M:%S')

        data_frame.insert(len(data_frame.columns), 'load', 0, True)

        self.data_combiner = DataCombiner(test_csv_path)
        data_frame = self.data_combiner.preprocess_data(data_frame)

        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame.to_sql(name='TestData', con=self.connection, if_exists='replace')
        self.connection.close()


    def load_test_data(self, from_date, to_date):
        self.connection = sqlite3.connect(DATABASE_NAME)
        query = 'SELECT * FROM TestData WHERE date >= ? and date <= ?'
        parameters = [from_date, to_date]

        data_frame = pd.read_sql_query(query, params=parameters, con=self.connection)
        self.connection.close()

        data_frame = data_frame.drop(['index'], axis=1)
        data_frame = data_frame.drop(['date'], axis=1)

        return data_frame
