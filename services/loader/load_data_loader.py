import pandas as pd
import os

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
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',', header=0, usecols=[0, 2, 4], names=['date', 'name', 'load'])

                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)


    def __filter_data(self):
        self.data_frame = self.data_frame.loc[self.data_frame['name'] == TARGETED_CITY]

        self.data_frame = self.data_frame.drop('name', axis=1)

        self.data_frame = self.data_frame[self.data_frame['date'].str.endswith("00:00")]

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%m/%d/%Y %H:%M:%S')

