import sqlite3
import pandas as pd


DATABASE_NAME = 'database/load_database.sqlite'

class DatabaseController():
    def __init__(self):
        pass


    def save_to_db(self, data_frame:pd.DataFrame):
        self.connection = sqlite3.connect(DATABASE_NAME)
        data_frame.to_sql(name='Load', con=self.connection, if_exists='replace')
        self.connection.close()
