import numpy
from sklearn.preprocessing import MinMaxScaler

class CustomPreparer:
    def __init__(self, data_frame, number_of_columns, share_for_training):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.datasetOrig = data_frame.values
        self.datasetOrig = self.datasetOrig.astype('float32')
        self.number_of_columns = number_of_columns
        self.predictor_column_no = self.number_of_columns - 1
        self.share_for_training = share_for_training
