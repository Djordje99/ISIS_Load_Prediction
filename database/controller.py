import sqlite3
import pandas as pd

from services.preprocessing.data_combiner import DataCombiner


DATABASE_NAME = 'database/load_database.db'


class DatabaseController():
    def save_to_db(self, folder_path):
        self.data_combiner = DataCombiner(folder_path)
        self.data_frame = self.data_combiner.generate_training_data()

        self.connection = sqlite3.connect(DATABASE_NAME)
        self.data_frame.to_sql(name='Load', con=self.connection, if_exists='replace')
        self.connection.close()


    def get_max_min_dates(self):
        return self.data_frame['date'].max(), self.data_frame['date'].min()


    def get_data_frame(self):
        return self.data_frame


    def load_data(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        #set max min date in sql
        self.data_frame = pd.read_sql_query('SELECT * FROM Load', self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        #self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%d %H:%M:%S')

        return self.data_frame


    def get_data_frame_from_date(self, from_date, to_date):
        self.connection = sqlite3.connect(DATABASE_NAME)
        #set max min date in sql
        query = 'SELECT * FROM Load WHERE date >= ? and date <= ?'
        parameters = [from_date, to_date]

        self.data_frame = pd.read_sql_query(query, params=parameters, con=self.connection)
        self.connection.close()

        self.data_frame = self.data_frame.drop(['index'], axis=1)
        self.data_frame = self.data_frame.drop(['date'], axis=1)

        #self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%d %H:%M:%S')

        return self.data_frame