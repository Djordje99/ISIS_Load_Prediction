from services.preprocessing.weather.weather_data_loader import WeatherDataLoader
from services.preprocessing.load.load_data_loader import LoadDataLoader

import pandas as pd
# import os
# import math

# NY_WEATHER_FOLDER = 'ISIS_Load_Prediction\\Training_Data\\NYS_Weather_Data\\New_York_City_NY'
# NY_LOAD_FOLDER = 'ISIS_Load_Prediction\\Training_Data\\NYS_Load_Data'
# PREPROCESSED_DATA_PATH = 'ISIS_Load_Prediction\\preprocessed_data'

# CSV_PART_SIZE = 8760

LOAD_PATH = 'NYS_Load_Data'
WEATHER_PATH = 'NYS_Weather_Data\\New_York_City_NY'

class DataCombiner():
    def __init__(self, folder_path) -> None:
        # path = os.getcwd()
        # dirname = os.path.abspath(os.path.join(path, os.pardir))

        # weather_path = os.path.join(dirname, NY_WEATHER_FOLDER)
        # load_path = os.path.join(dirname, NY_LOAD_FOLDER)
        # self.preprocessed_path = os.path.join(dirname, PREPROCESSED_DATA_PATH)

        # self.load_loader = LoadDataLoader(load_path)
        # self.weather_loader = WeatherDataLoader(weather_path)
        # self.preprocessed_loader = LoadPreprocessedData(self.preprocessed_path)
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


    # def __save_to_csv(self, data_frame:pd.DataFrame) -> None:
    #     csv_size = len(data_frame)
    #     file_count = math.floor(csv_size / CSV_PART_SIZE) + 1

    #     for i in range(round(file_count)):
    #         date_frame_temp = data_frame[CSV_PART_SIZE * i : CSV_PART_SIZE * (i + 1)]
    #         date_frame_temp.to_csv(f'preprocessed_data\\training_data_{i + 1}.csv', index=False)


    # def __check_preprocessed_data(self) -> bool:
    #     dirs = os.listdir(self.preprocessed_path)
    #     if len(dirs) == 0:
    #         return False
    #     else:
    #         return True


    def generate_training_data(self) -> pd.DataFrame:
        load_data_frame = self.__load_load_data()
        weather_data_frame = self.__load_weather_data(load_data_frame['date'].min(), load_data_frame['date'].max())

        training_data = pd.merge_asof(weather_data_frame, load_data_frame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
        training_data = training_data[training_data['load'].notna()]
        training_data = training_data.reset_index(drop=True)
        #self.__save_to_csv(training_data)

        print(training_data)

        return training_data


    # def get_training_data(self):
    #     if self.__check_preprocessed_data():
    #         return self.preprocessed_loader.load_data()
    #     else:
    #         return self.__generate_training_data()
