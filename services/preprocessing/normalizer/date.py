
class DateNormalizer():
    def __init__(self, data_frame) -> None:
        self.data_frame = data_frame


    def __create_hour_column(self):
        date_hours = self.data_frame['date'].dt.hour
        self.data_frame.insert(1, 'datehour', date_hours)


    def __create_day_column(self):
        date = self.data_frame['date']
        self.data_frame.insert(1, 'day', date.apply(lambda x: x.weekday()))


    def normalize_date(self):
        self.__create_hour_column()
        self.__create_day_column()

        self.data_frame = self.data_frame.drop(['date'], axis=1)

        return self.data_frame