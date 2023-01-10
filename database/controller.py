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


    def save_to_db(self, folder_path, mode):
        self.connection = sqlite3.connect(DATABASE_NAME)
        previous_data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        previous_data_frame['date'] = pd.to_datetime(previous_data_frame['date'])
        self.connection.close()

        self.data_combiner = DataCombiner(folder_path)
        if mode == 'append':
            self.data_frame = self.data_combiner.generate_training_data(previous_data_frame)
        else:
            self.data_frame = self.data_combiner.generate_training_data()

        print(self.data_frame)

        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists=mode)
        self.connection.close()


    def load_data(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


    def get_data_frame_from_date(self, from_date, to_date):
        self.connection = sqlite3.connect(DATABASE_NAME)
        query = 'SELECT * FROM Load WHERE date >= ? and date <= ?'
        parameters = [from_date, to_date]

        self.data_frame = pd.read_sql_query(query, params=parameters, con=self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


    def save_predicted_load(self, y_predicted, date_from, day_number):
        date_from += ' 00:00:00'
        dates = pd.date_range(date_from, periods=day_number*24, freq='H')

        #data_frame['date'] = dates

        #data_frame['predicted_load'] = y_predicted

        data_frame = pd.DataFrame({'date': dates, 'predicted_load': y_predicted.ravel()})

        data_frame = data_frame.set_index('date', drop=True)

        print(data_frame)

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


        print(data_frame.head())

        self.data_combiner = DataCombiner(test_csv_path)
        data_frame = self.data_combiner.preprocess_data(data_frame)

        data_frame = data_frame.drop(['name'], axis=1)

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
