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


    def save_predicted_load(self, y_predicted, date_from, date_to):
        data_frame = pd.DataFrame()

        date_from += ' 00:00:00'
        date_to += ' 00:00:00'
        dates = pd.date_range(date_from, date_to, freq='H')

        data_frame['date'] = dates

        last_row = data_frame.tail(1)
        data_frame = data_frame.drop(last_row.index)

        data_frame['predicted_load'] = y_predicted

        data_frame = data_frame.set_index('date', drop=True)

        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame.to_sql(name='PredictedLoad', con=self.connection, if_exists='replace')
        self.connection.close()


    def load_predicted_load(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame = pd.read_sql_query('SELECT * FROM PredictedLoad', self.connection)
        self.connection.close()

        return data_frame
