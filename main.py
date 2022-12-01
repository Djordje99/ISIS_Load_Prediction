from services.preprocessing.weather_data_loader import WeatherDataLoader
from services.preprocessing.load_data_loader import LoadDataLoader


NY_WEATHER_PATH = 'D:\\GitHub\\ISIS_Load_Prediction\\Training_Data\\NYS_Weather_Data\\New_York_City_NY'
NY_LOAD_PATH = 'D:\\GitHub\\ISIS_Load_Prediction\\Training_Data\\NYS_Load_Data'


if __name__ == '__main__':
    loader = LoadDataLoader(NY_LOAD_PATH)
    data_frame = loader.load_data()

    print(data_frame)