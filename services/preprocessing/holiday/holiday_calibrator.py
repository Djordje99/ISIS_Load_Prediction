import pandas as pd
import numpy as np

HOLIDAY_DATES_2018 = [
    "2018-01-01", # New Year's Day
    "2018-01-15", # Martin Luther King Jr. Day
    "2018-02-14", # Valentine's Day
    "2018-02-19", # Presidents' Day
    "2018-03-17", # St. Patrick's Day
    "2018-04-01", # April Fool's Day
    "2018-05-13", # Mother's Day
    "2018-05-28", # Memorial Day
    "2018-06-17", # Father's Day
    "2018-07-04", # Independence Day
    "2018-09-03", # Labor Day
    "2018-10-08", # Columbus Day
    "2018-10-31", # Halloween
    "2018-11-11", # Veterans Day
    "2018-11-22", # Thanksgiving Day
    "2018-12-24", # Christmas Eve
    "2018-12-25", # Christmas Day
    "2018-12-31"  #New year eve
]

HOLIDAY_DATES_2019 = [
    "2019-01-01", # New Year's Day
    "2019-01-21", # Martin Luther King Jr. Day
    "2019-02-14", # Valentine's Day
    "2019-02-18", # Presidents' Day
    "2019-03-17", # St. Patrick's Day
    "2019-04-01", # April Fool's Day
    "2019-05-12", # Mother's Day
    "2019-05-27", # Memorial Day
    "2019-06-16", # Father's Day
    "2019-07-04", # Independence Day
    "2019-09-02", # Labor Day
    "2019-10-14", # Columbus Day
    "2019-10-31", # Halloween
    "2019-11-11", # Veterans Day
    "2019-11-28", # Thanksgiving Day
    "2019-12-24", # Christmas Eve
    "2019-12-25", # Christmas Day
    "2019-12-31"  #New year eve
]

HOLIDAY_DATES_2020 = [
    "2020-01-01", # New Year's Day
    "2020-01-20", # Martin Luther King Jr. Day
    "2020-02-14", # Valentine's Day
    "2020-02-17", # Presidents' Day
    "2020-03-17", # St. Patrick's Day
    "2020-04-01", # April Fool's Day
    "2020-05-10", # Mother's Day
    "2020-05-25", # Memorial Day
    "2020-06-21", # Father's Day
    "2020-07-04", # Independence Day
    "2020-09-07", # Labor Day
    "2020-10-12", # Columbus Day
    "2020-10-31", # Halloween
    "2020-11-11", # Veterans Day
    "2020-11-26", # Thanksgiving Day
    "2020-12-24", # Christmas Eve
    "2020-12-25", # Christmas Day
    "2020-12-31"  #New year eve
]

HOLIDAY_DATES_2021 = [
    "2021-01-01", # New Year's Day
    "2021-01-18", # Martin Luther King Jr. Day
    "2021-02-14", # Valentine's Day
    "2021-02-15", # Presidents' Day
    "2021-03-17", # St. Patrick's Day
    "2021-04-01", # April Fool's Day
    "2021-05-09", # Mother's Day
    "2021-05-31", # Memorial Day
    "2021-06-20", # Father's Day
    "2021-07-04", # Independence Day
    "2021-09-06", # Labor Day
    "2021-10-11", # Columbus Day
    "2021-10-31", # Halloween
    "2021-11-11", # Veterans Day
    "2021-11-25", # Thanksgiving Day
    "2021-12-24", # Christmas Eve
    "2021-12-25", # Christmas Day
    "2021-12-31"  #New year eve
]

HOLIDAYS_2018_2021 = [HOLIDAY_DATES_2018, HOLIDAY_DATES_2019, HOLIDAY_DATES_2020, HOLIDAY_DATES_2021]

class HolidayCalibrator():
    def __init__(self) -> None:
        pass

    def calibrate_holidays(self, data_frame:pd.DataFrame):
        data_frame.insert(2, 'is_holiday', np.zeros(len(data_frame)))

        # holidays_2018_2021 = []
        # holidays_2018_2021.extend(HOLIDAY_DATES_2018)
        # holidays_2018_2021.extend(HOLIDAY_DATES_2019)
        # holidays_2018_2021.extend(HOLIDAY_DATES_2020)
        # holidays_2018_2021.extend(HOLIDAY_DATES_2021)

        # holidays_2018_2021 = pd.date_range(dates=holidays_2018_2021)

        # for holiday in holidays_2018_2021:
        #     if holiday in data_frame['date'].dt.date.values:
        #         date = data_frame['date'].dt.date
        #         indexes = data_frame[date == holiday].index
        #         data_frame.iloc[[indexes], [2]] = 1

        # for holiday_year in HOLIDAYS_2018_2021:
        #     for holiday in holiday_year:
        #         date = data_frame['date'].dt.date
        #         holiday_date = pd.to_datetime(holiday)
        #         indexes = data_frame[date == holiday_date].index
        #         data_frame.iloc[[indexes], [2]] = 1

        holiday_dates = [pd.to_datetime(holiday).date() for holiday_year in HOLIDAYS_2018_2021 for holiday in holiday_year]
        data_frame.loc[data_frame['date'].dt.date.isin(holiday_dates), 'is_holiday'] = 1

        return data_frame