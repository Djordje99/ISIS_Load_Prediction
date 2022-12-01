from services.preprocessing.weather_data_loader import WeatherDataLoader

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

NY_WEATHER_PATH = 'D:\\GitHub\\ISIS_Load_Prediction\\Training_Data\\NYS_Weather_Data\\New_York_City_NY'

class WeatherDataPreprocessor():
    def __init__(self) -> None:
        loader = WeatherDataLoader(NY_WEATHER_PATH)
        self.data_frame = loader.load_data()

    def preprocessing_data(self):
        pass