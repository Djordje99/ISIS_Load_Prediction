from services.preprocessing.data_combiner import DataCombiner

import pandas as pd
import numpy as np

class TemperatureCalibrator():
    def __init__(self):
        pass


    def fill_missing_value(self, data_frame):
        temp = data_frame.loc[data_frame['temp'] >= 122]
        temp = pd.concat([temp, data_frame.loc[data_frame['temp'] <= -23]])

        for index, row in temp.iterrows():
            temp_sum = data_frame.iloc[index-1]['temp'] + data_frame.iloc[index+1]['temp']
            new_temp = temp_sum / 2

            data_frame.at[index, 'temp'] = round(new_temp, 1)

        return data_frame

    #TODO add mean temperature to data frame
    def fill_mean_temperature(self, data_frame:pd.DataFrame):
        #means = data_frame.groupby([data_frame['date'].dt.date], as_index=False).mean()
        means = data_frame.resample('temp', on='date').mean()
        print(means)

        return data_frame