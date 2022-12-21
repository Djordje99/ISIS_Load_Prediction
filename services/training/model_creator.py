from services.preprocessing.preparer import Preparer
from database.controller import DatabaseController
from services.training.ann_regression import AnnRegression
from services.scorer.scrorer import Scorer
from services.scorer.ploting import CustomPloting
from time import time


NUMBER_OF_COLUMNS = 26
SHARE_FOR_TRAINING = 0.85


class ModelCreator():
    def __init__(self) -> None:
        self.controller = DatabaseController()
        self.preparer = Preparer(self.controller.load_data_frame(), NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING)


    def create_model(self):
        trainX, trainY, testX, testY = self.preparer.prepare_for_training()

        # make predictions
        ann_regression = AnnRegression()

        time_begin = time()

        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)

        time_end = time()

        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

        # invert predictions
        trainPredict, trainY, testPredict, testY = self.preparer.inverse_transform(trainPredict, testPredict)

        # calculate root mean squared error
        scorer = Scorer()
        trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))

        # plotting
        custom_plotting = CustomPloting()
        custom_plotting.show_plots(testPredict, testY)
