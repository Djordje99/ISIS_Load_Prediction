import pandas as pd
import numpy as np


class LoadCalibrator():
    def __init__(self):
        pass

    def create_previous_day_load_feature(self, data_frame:pd.DataFrame):
        daily_mean = data_frame.groupby([data_frame['date'].dt.date]).mean()['load'].reset_index(name='load')

        daily_mean['date'] = pd.to_datetime(daily_mean['date'])

        year_mean = daily_mean.groupby([daily_mean['date'].dt.year]).mean()['load'].reset_index()

        data_frame.insert(2, 'previous_day_mean_load', np.nan)

        print(year_mean)

        for i, row in daily_mean.iterrows():
            if i < 1:
                indexs = data_frame[data_frame['date'].dt.year == year_mean['date'][0]].index
                data_frame.iloc[[indexs], [2]] = year_mean['load'][0]
            else:
                indexs = data_frame[data_frame['date'].dt.date == daily_mean['date'].dt.date[i]].index
                data_frame.iloc[[indexs], [2]] = daily_mean['load'][i - 1]

        return data_frame

    def create_previous_weekday_load_feature(self, data_frame:pd.DataFrame):
        year_mean = data_frame.groupby([data_frame['date'].dt.year]).mean()['load'].reset_index()

        data_frame.insert(2, 'previous_weekday_load', np.nan)

        data_frame['previous_weekday_load'] = data_frame['load'].shift(periods=168)

        for i in range(0, 168):
            data_frame['previous_weekday_load'][i] = year_mean['load'][0]

        data_frame.insert(2, 'previous_day_load', np.nan)

        data_frame['previous_day_load'] = data_frame['load'].shift(periods=24)

        for i in range(0, 24):
            data_frame['previous_day_load'][i] = year_mean['load'][0]

        return data_frame
