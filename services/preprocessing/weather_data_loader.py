import pandas as pd
import numpy as np
import os

class WeatherDataLoader():
    def __init__(self, input_path) -> None:
        self.input_path = input_path


    def load_data(self):
        data_frame = pd.DataFrame()

        for filename in os.scandir(self.input_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',', header=None)
                data_frame = pd.concat([data_frame, data_frame_temp], axis=0)

        return data_frame
