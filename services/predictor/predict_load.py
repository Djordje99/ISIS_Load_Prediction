from services.training.ann_regression import AnnRegression
from database.controller import DatabaseController
from services.scorer.scrorer import Scorer
from services.preprocessing.preparer import Preparer

import numpy as np

TRAINING_SHARE = 0.85
MAX_LOAD = 11110.3
MIN_LOAD = 3589.2


class LoadPredictor():
    def __init__(self) -> None:
        self.controller = DatabaseController()
        self.ann_regression = AnnRegression()
        self.scorer = Scorer()
        self.data_preparer = Preparer(TRAINING_SHARE)


    def predict(self, date_form, date_to, day_number):
        X_test, y_test = self.data_preparer.prepare_predict_date(date_form, date_to)

        y_predicted = self.ann_regression.predict(X_test)

        y_predicted = self.data_preparer.scaled_to_original(y_predicted)
        y_test = self.data_preparer.scaled_to_original(y_test)

        rmsr = self.scorer.get_mean_square_error(y_test.ravel(), y_predicted.ravel())
        print(f"RMSR Accuracy: {rmsr}")

        mape = self.scorer.get_mean_absolute_percentage_error(y_test.ravel(), y_predicted.ravel())
        print(f'MAPE Accuracy: {mape}%')

        #SAVE TO DATABASE PREDICTION
        self.controller.save_predicted_load(y_predicted, date_form, day_number)


    def predict_test_data(self, date_form, date_to, day_number):
        X_test, y_test = self.data_preparer.prepare_test_data(date_form, date_to)

        y_predicted = self.ann_regression.predict(X_test)

        y_predicted = self.data_preparer.scaled_to_original(y_predicted)
        self.controller.save_predicted_load(y_predicted, date_form, day_number)