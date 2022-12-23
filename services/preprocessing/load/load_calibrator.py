import pandas as pd
import numpy as np


class LoadCalibrator():
    def __init__(self):
        pass

    def create_last_load_feature(self, data_frame:pd.DataFrame):
        dates = data_frame.groupby([data_frame['date'].dt.date]).mean()['load'].reset_index(name='load')

        print(dates.head())

        # for i, row in data_frame.iterrows():
        #     indexs = data_frame[data_frame['date'].dt.date == means['date'].dt.date[i]].index
        #     data_frame.iloc[[indexs], [2]] = means['temp'][i]
        #     data_frame.iloc[[indexs], [4]] = maxs['temp'][i]
        #     data_frame.iloc[[indexs], [5]] = mins['temp'][i]




        # means = data_frame.groupby([data_frame['date'].dt.date]).mean()['temp'].reset_index(name='temp')
        # maxs = data_frame.groupby([data_frame['date'].dt.date]).max()['temp'].reset_index(name='temp')
        # mins = data_frame.groupby([data_frame['date'].dt.date]).min()['temp'].reset_index(name='temp')

        # means['date'] = pd.to_datetime(means['date'])
        # maxs['date'] = pd.to_datetime(means['date'])
        # mins['date'] = pd.to_datetime(means['date'])

        # data_frame.insert(2, 'meantemp', np.nan)
        # data_frame.insert(4, 'maxtemp', np.nan)
        # data_frame.insert(5, 'mintemp', np.nan)

        # print(means)

        # for i, row in means.iterrows():
        #     indexs = data_frame[data_frame['date'].dt.date == means['date'].dt.date[i]].index
        #     data_frame.iloc[[indexs], [2]] = means['temp'][i]
        #     data_frame.iloc[[indexs], [4]] = maxs['temp'][i]
        #     data_frame.iloc[[indexs], [5]] = mins['temp'][i]


        # return data_frame