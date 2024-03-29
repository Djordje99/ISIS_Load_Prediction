from services.preprocessing.preparer import Preparer
from database.controller import DatabaseController
from services.training.ann_regression import AnnRegression
from services.scorer.scrorer import Scorer
from services.scorer.ploting import CustomPloting
from time import time

SHARE_FOR_TRAINING = 0.85


class ModelCreator():
    def __init__(self) -> None:
        self.preparer = Preparer(SHARE_FOR_TRAINING)


    def create_model(self, date_from, date_to):
        trainX, trainY, testX, testY = self.preparer.prepare_for_training(date_from, date_to)

        ann_regression = AnnRegression()

        time_begin = time()

        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX, trainX.shape[2])

        time_end = time()

        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

        #trainPredict, trainY, testPredict, testY = self.preparer.inverse_transform(trainPredict, testPredict)

        trainY = self.preparer.scaled_to_original(trainY)
        testY = self.preparer.scaled_to_original(testY)
        trainPredict = self.preparer.scaled_to_original(trainPredict)
        testPredict = self.preparer.scaled_to_original(testPredict)

        # trainPredict = self.preparer.scale_load_original(trainPredict)
        # trainY = self.preparer.scale_load_original(trainY)
        # testPredict = self.preparer.scale_load_original(testPredict)
        # testY = self.preparer.scale_load_original(testY)

        scorer = Scorer()
        trainScore, testScore = scorer.get_rmse_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))

        print()

        trainScore, testScore = scorer.get_mape_score(trainY, trainPredict, testY, testPredict)
        print(f'Train Score: {round(trainScore, 2)}% MARE')
        print(f'Test Score: {round(testScore, 2)}% MARE')

        # custom_plotting = CustomPloting()
        # custom_plotting.show_plots(testPredict, testY)

        return testPredict, testY
