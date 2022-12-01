import pandas as pd
import numpy as np
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
            break

        return self.__filter_data()


    def __load_folder_data(self, folder_path):
        for filename in os.scandir(folder_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',', header=None)
                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)


    def __filter_data(self):
        self.data_frame = self.data_frame.loc[self.data_frame[2] == TARGETED_CITY]

        self.data_frame = self.data_frame.loc[self.data_frame[0] == '01/01/2018 00:00:00']


