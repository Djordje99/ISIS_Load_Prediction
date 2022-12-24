from services.training.ann_regression import AnnRegression
from database.controller import DatabaseController
from services.scorer.scrorer import Scorer
from services.scorer.ploting import CustomPloting
from services.preprocessing.preparer import Preparer

TRAINING_SHARE = 0.85

class LoadPredictor():
    def __init__(self) -> None:
        self.controller = DatabaseController()
        self.ann_regression = AnnRegression()
        self.scorer = Scorer()
        self.ploting = CustomPloting()
        self.data_preparer = Preparer(TRAINING_SHARE)


    def predict(self, from_date, to_date):
        X_test, y_test = self.data_preparer.prepare_predict_date(from_date, to_date)

        y_predict = self.ann_regression.predict(X_test)

        y_predict, y_test = self.data_preparer.inverse_predict_transform(y_predict)

        rmsr = self.scorer.get_mean_square_error(y_test, y_predict)
        print(f"RMSR Accuracy: {rmsr}")

        mape = self.scorer.get_mean_absolute_percentage_error(y_test, y_predict)
        print(f'MAPE Accuracy: {mape}%')

        self.ploting.show_plots(y_predict, y_test)

        #SAVE TO DATABASE PREDICTION

