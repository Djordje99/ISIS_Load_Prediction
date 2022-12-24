import pandas as pd

FEATURE_DROP = ['precip', 'windgust', 'winddir', 'dew', 'sealevelpressure','precipprob','preciptype','snow','snowdepth', 'visibility','solarradiation','solarenergy','uvindex','severerisk']

class WeatherCalibrator():
    def interpolate_missing_value(self, data_frame:pd.DataFrame):
        data_frame['feelslike'] = data_frame['feelslike'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['windspeed'] = data_frame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['humidity'] = data_frame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        #data_frame['windgust'] = data_frame['windgust'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        #data_frame['winddir'] = data_frame['winddir'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['cloudcover'] = data_frame['cloudcover'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")

        #data_frame['dew'] = data_frame['dew'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        #data_frame['sealevelpressure'] = data_frame['sealevelpressure'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")

        return data_frame

    def drop_features(self, data_frame):
        data_frame = data_frame.drop(FEATURE_DROP, axis=1)
        return data_frame