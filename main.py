from services.preprocessing.weather_data_loader import WeatherDataLoader
from services.preprocessing.load_data_loader import LoadDataLoader

import pandas as pd
import math

NY_WEATHER_PATH = 'D:\\GitHub\\ISIS_Load_Prediction\\Training_Data\\NYS_Weather_Data\\New_York_City_NY'
NY_LOAD_PATH = 'D:\\GitHub\\ISIS_Load_Prediction\\Training_Data\\NYS_Load_Data'
CSV_PART_SIZE = 8760


if __name__ == '__main__':
    load_loader = LoadDataLoader(NY_LOAD_PATH)
    weather_loader = WeatherDataLoader(NY_WEATHER_PATH)

    load_data_frame = load_loader.load_data()
    print(load_data_frame)

    weather_data_frame = weather_loader.load_data(load_data_frame[0].min(), load_data_frame[0].max())
    print(weather_data_frame)

    load_data_frame = load_data_frame.reset_index(drop=True)
    weather_data_frame = weather_data_frame.reset_index(drop=True)

    training_data = pd.concat([weather_data_frame, load_data_frame[4]], axis=1)

    print(training_data)

    csv_size = len(training_data)
    file_count = math.floor(csv_size / CSV_PART_SIZE) + 1

    for i in range(round(file_count)):
        date_frame_temp = training_data[CSV_PART_SIZE * i : CSV_PART_SIZE * (i + 1)]
        date_frame_temp.to_csv(f'preprocessed_data\\training_data_{i + 1}.csv', index=False)