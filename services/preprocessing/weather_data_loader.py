import pandas as pd
import numpy as np
import os

class WeatherDataLoader():
    def __init__(self, input_path) -> None:
        self.input_path = input_path
        self.data_frame = pd.DataFrame()


    def load_data(self, min_date, max_date):
        for filename in os.scandir(self.input_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',', header=None)
                data_frame_temp = data_frame_temp.drop(0) #drop header
                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)

        self.data_frame[1] = pd.to_datetime(self.data_frame[1], format='%Y-%m-%dT%H:%M:%S')

        self.__filter_by_date(min_date, max_date)

        return self.data_frame


    def __filter_by_date(self, min_date, max_date):
        mask = self.data_frame[1].between(min_date, max_date)
        self.data_frame = self.data_frame.loc[mask]

        print(self.data_frame)
