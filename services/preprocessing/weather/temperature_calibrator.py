import pandas as pd
import numpy as np

class TemperatureCalibrator():
    def __init__(self):
        pass


    def fill_missing_value(self, data_frame:pd.DataFrame):
        temp = data_frame.loc[data_frame['temp'] >= 122]
        temp = pd.concat([temp, data_frame.loc[data_frame['temp'] <= -23]])

        for index, row in temp.iterrows():
            temp_sum = data_frame.iloc[index-1]['temp'] + data_frame.iloc[index+1]['temp']
            new_temp = temp_sum / 2

            data_frame.at[index, 'temp'] = round(new_temp, 1)

        return data_frame


    def create_additional_temperature_feature(self, data_frame:pd.DataFrame):
        means = data_frame.groupby([data_frame['date'].dt.date]).mean()['temp'].reset_index(name='temp')
        maxs = data_frame.groupby([data_frame['date'].dt.date]).max()['temp'].reset_index(name='temp')
        mins = data_frame.groupby([data_frame['date'].dt.date]).min()['temp'].reset_index(name='temp')

        means['date'] = pd.to_datetime(means['date'])
        maxs['date'] = pd.to_datetime(means['date'])
        mins['date'] = pd.to_datetime(means['date'])

        data_frame.insert(2, 'mean_temp', np.nan)
        data_frame.insert(4, 'max_temp', np.nan)
        data_frame.insert(5, 'min_temp', np.nan)

        print(means)

        for i, row in means.iterrows():
            indexs = data_frame[data_frame['date'].dt.date == means['date'].dt.date[i]].index
            data_frame.iloc[[indexs], [2]] = means['temp'][i]
            data_frame.iloc[[indexs], [4]] = maxs['temp'][i]
            data_frame.iloc[[indexs], [5]] = mins['temp'][i]


        return data_frame


    def create_mean_temperature_previous_day(self, data_frame:pd.DataFrame):
        data_frame.insert(2, 'mean_temp_previous_day', np.nan)
        data_frame.insert(4, 'max_temp_previous_day', np.nan)
        data_frame.insert(5, 'min_temp_previous_day', np.nan)

        data_frame['mean_temp_previous_day'] = data_frame['mean_temp'].shift(24).fillna(0)
        data_frame['max_temp_previous_day'] = data_frame['max_temp'].shift(24).fillna(0)
        data_frame['min_temp_previous_day'] = data_frame['min_temp'].shift(24).fillna(0)

        return data_frame