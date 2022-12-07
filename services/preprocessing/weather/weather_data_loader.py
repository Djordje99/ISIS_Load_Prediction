import pandas as pd
import os

class WeatherDataLoader():
    def __init__(self, input_path) -> None:
        self.input_path = input_path
        self.data_frame = pd.DataFrame()


    def load_data(self, min_date, max_date):
        for filename in os.scandir(self.input_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',',
                names=['name','date','temp','feelslike','dew','humidity','precip','precipprob','preciptype','snow','snowdepth','windgust','windspeed','winddir',
                'sealevelpressure','cloudcover','visibility','solarradiation','solarenergy','uvindex','severerisk','conditions'])

                data_frame_temp = data_frame_temp.drop(0)
                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%dT%H:%M:%S')

        self.__filter_by_date(min_date, max_date)

        return self.data_frame


    def __filter_by_date(self, min_date, max_date):
        mask = self.data_frame['date'].between(min_date, max_date)
        self.data_frame = self.data_frame.loc[mask]
