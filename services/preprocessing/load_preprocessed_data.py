import pandas as pd
import os


class LoadPreprocessedData():
    def __init__(self, path) -> None:
        self.data_path = path
        self.data_frame = pd.DataFrame()


    def load_data(self) -> pd.DataFrame:
        for filename in os.scandir(self.data_path):
            if filename.is_file() and filename.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(filename.path, engine='python', sep=',',
                    names=['date','temp','feelslike','dew','humidity','precip','precipprob','preciptype','snow','snowdepth','windgust','windspeed','winddir',
                        'sealevelpressure','cloudcover','visibility','solarradiation','solarenergy','uvindex','severerisk','conditions','PTID','load'])

                data_frame_temp = data_frame_temp.drop(0)
                self.data_frame = pd.concat([self.data_frame, data_frame_temp], axis=0)

        self.data_frame['date'] = pd.to_datetime(self.data_frame['date'], format='%Y-%m-%dT%H:%M:%S')
        self.data_frame['temp'] = pd.to_numeric(self.data_frame['temp'])

        self.data_frame = self.data_frame.reset_index(drop=True)

        return self.data_frame
