import pandas as pd


class WeatherCalibrator():
    def interpolate_missing_value(self, data_frame:pd.DataFrame):
        data_frame['dew'] = data_frame['dew'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['windspeed'] = data_frame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['humidity'] = data_frame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['windgust'] = data_frame['windgust'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['winddir'] = data_frame['winddir'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['cloudcover'] = data_frame['cloudcover'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")

        return data_frame