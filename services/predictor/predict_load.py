from services.training.ann_regression import AnnRegression
from database.controller import DatabaseController
from services.scorer.scrorer import Scorer
from services.preprocessing.preparer import Preparer

TRAINING_SHARE = 0.85

class LoadPredictor():
    def __init__(self) -> None:
        self.controller = DatabaseController()
        self.ann_regression = AnnRegression()
        self.scorer = Scorer()
        self.data_preparer = Preparer(TRAINING_SHARE)


    def predict(self, date_form, date_to):
        X_test, y_test = self.data_preparer.prepare_predict_date(date_form, date_to)

        y_predicted = self.ann_regression.predict(X_test)

        y_predicted, y_test = self.data_preparer.inverse_predict_transform(y_predicted)

        rmsr = self.scorer.get_mean_square_error(y_test, y_predicted)
        print(f"RMSR Accuracy: {rmsr}")

        mape = self.scorer.get_mean_absolute_percentage_error(y_test, y_predicted)
        print(f'MAPE Accuracy: {mape}%')

        #SAVE TO DATABASE PREDICTION
        self.controller.save_predicted_load(y_predicted, date_form, date_to)

