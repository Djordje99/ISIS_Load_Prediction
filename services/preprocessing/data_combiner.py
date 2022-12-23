from services.loader.weather_data_loader import WeatherDataLoader
from services.loader.load_data_loader import LoadDataLoader

import pandas as pd

LOAD_PATH = 'NYS_Load_Data'
WEATHER_PATH = 'NYS_Weather_Data\\New_York_City_NY'


class DataCombiner():
    def __init__(self, folder_path) -> None:
        self.load_loader = LoadDataLoader(f'{folder_path}\{LOAD_PATH}')
        self.weather_loader = WeatherDataLoader(f'{folder_path}\{WEATHER_PATH}')


    def __load_load_data(self) -> pd.DataFrame:
        load_data_frame = self.load_loader.load_data()
        load_data_frame = load_data_frame.reset_index(drop=True)

        return load_data_frame


    def __load_weather_data(self, min_date, max_date) -> pd.DataFrame:
        weather_data_frame = self.weather_loader.load_data(min_date, max_date)
        weather_data_frame = weather_data_frame.reset_index(drop=True)

        weather_data_frame = weather_data_frame.drop('name', axis=1)

        return weather_data_frame


    def generate_training_data(self) -> pd.DataFrame:
        load_data_frame = self.__load_load_data()
        weather_data_frame = self.__load_weather_data(load_data_frame['date'].min(), load_data_frame['date'].max())

        training_data = pd.merge_asof(weather_data_frame, load_data_frame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
        training_data = training_data[training_data['load'].notna()]
        training_data = training_data.reset_index(drop=True)

        print(training_data)

        return training_data
