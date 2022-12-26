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
        date = self.data_frame['date'].dt.date
        seasons = pd.DataFrame()
        seasons['seasons'] = date.apply(get_seasons)

        seasons_encoded = pd.get_dummies(seasons.seasons, prefix='season')

        for name in seasons_encoded.columns:
            self.data_frame.insert(1, name, seasons_encoded[name])


    def normalize_date(self):
        self.__create_hour_column()
        self.__create_weekday_column()
        self.__create_month_column()
        self.__cerate_season_column()

        #self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame


def get_seasons(date):
    month = date.month
    day = date.day

    if month in [12, 1, 2] or (month == 3 and day < 21):
        return "winter"
    elif month in [3, 4, 5] or (month == 6 and day < 21):
        return "spring"
    elif month in [6, 7, 8] or (month == 9 and day < 23):
        return "summer"
    else:
        return "autumn"