import numpy as np
import pandas as pd


SECONDS_IN_DAY = 24*60*60
WEEKDAYS = 7
MONTH = 12
SEASON = 4


class DateNormalizer():
    def __init__(self, data_frame) -> None:
        self.data_frame = data_frame


    def __create_hour_column(self):
        hours = self.data_frame['date'].dt.hour
        seconds = hours.apply(lambda x: x*60*60)

        sin_date = np.sin(seconds*(2*np.pi/SECONDS_IN_DAY))
        cos_time = np.cos(seconds*(2*np.pi/SECONDS_IN_DAY))

        self.data_frame.insert(1, 'sin_date', sin_date)
        self.data_frame.insert(1, 'cos_time', cos_time)


    def __create_weekday_column(self):
        date = self.data_frame['date']
        weekdays = date.apply(lambda x: x.weekday())

        sin_weekday = np.sin(weekdays*(2.*np.pi/WEEKDAYS))
        cos_weekday = np.cos(weekdays*(2.*np.pi/WEEKDAYS))

        self.data_frame.insert(1, 'sin_weekday', sin_weekday)
        self.data_frame.insert(1, 'cos_weekday', cos_weekday)


    def __create_month_column(self):
        month = self.data_frame['date'].dt.month

        sin_month = np.sin(month*(2.*np.pi/MONTH))
        cos_month = np.cos(month*(2.*np.pi/MONTH))

        self.data_frame.insert(1, 'sin_month', sin_month)
        self.data_frame.insert(1, 'cos_month', cos_month)


    def __cerate_season_column(self):
        month = self.data_frame['date'].dt.month
        seasons = pd.DataFrame()
        seasons['seasons'] = month.apply(get_seasons)

        seasons_encoded = pd.get_dummies(seasons.seasons, prefix='season')

        for name in seasons_encoded.columns:
            self.data_frame.insert(1, name, seasons_encoded[name])


    def normalize_date(self):
        self.__create_hour_column()
        self.__create_weekday_column()
        self.__create_month_column()
        self.__cerate_season_column()

        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


def get_seasons(month):
    if month == 12 or month == 1 or month == 2:
        return 'winter'
    elif month == 3 or month == 4 or month == 5:
        return 'spring'
    elif month == 6 or month == 7 or month == 8:
        return 'autumn'
    else:
        return 'summer'