import math
import numpy as np

from sklearn.metrics import mean_squared_error


class Scorer:
    def get_rmse_score(self, train_y, train_predict, test_y, test_predict):
        train_score = math.sqrt(mean_squared_error(train_y, train_predict))
        test_score = math.sqrt(mean_squared_error(test_y, test_predict))
        return train_score, test_score


    def get_mare_score(self, train_y, train_predict, test_y, test_predict):
        train_score = self.__mean_absolute_percentage_error(train_y, train_predict)
        test_score = self.__mean_absolute_percentage_error(test_y, test_predict)

        return train_score, test_score


    def __mean_absolute_percentage_error(self, y_actual, y_predicted):
        mape = np.mean(np.abs((y_actual - y_predicted)/y_actual))*100
        return mape