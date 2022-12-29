import pandas as pd
import os
import datetime

import logging
logging.basicConfig(filename="log.log", format='%(asctime)s %(message)s',filemode='w')
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TARGETED_CITY = 'N.Y.C.'

class LoadDataLoader():
    def __init__(self, input_path) -> None:
        self.input_path = input_path
        self.data_frame = pd.DataFrame()


    def load_data(self):
        for folder in os.scandir(self.input_path):
            data_frame_temp = self.__load_folder_data(folder)

            self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)
        self.__filter_data()

        return self.data_frame


    def __load_folder_data(self, folder_path):
        for filename in os.scandir(folder_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                logger.info(f'Loading {filename.name}...')
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',', header=0, usecols=[0, 2, 4], names=['date', 'name', 'load'])

                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)


    def __filter_data(self):
        self.data_frame = self.data_frame.loc[self.data_frame['name'] == TARGETED_CITY]

        self.data_frame = self.data_frame.drop('name', axis=1)

        print(self.data_frame.head())

        if((self.is_date_in_format(self.data_frame['date'].iloc[0], '%m/%d/%Y %H:%M'))):
            self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%m/%d/%Y %H:%M')
            self.data_frame['date'] = self.data_frame['date'].astype(str)
        else:
            self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%m/%d/%Y %H:%M:%S')
            self.data_frame['date'] = self.data_frame['date'].astype(str)

        print(self.data_frame.head())

        self.data_frame = self.data_frame[self.data_frame['date'].str.endswith("00:00")]

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y/%m/%d %H:%M:%S')


    def is_date_in_format(self, date_str, date_format):
        try:
            datetime.datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

