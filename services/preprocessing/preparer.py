import numpy
from sklearn.preprocessing import MinMaxScaler
from services.preprocessing.normalizer.date import DateNormalizer
from services.preprocessing.normalizer.missing_value import MissingValue
from services.preprocessing.normalizer.string import StringNormalizer


class Preparer:
    def __init__(self, data_frame, number_of_columns, share_for_training):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.date_normalizer = DateNormalizer(data_frame)
        data_frame = self.date_normalizer.normalize_date()

        self.string_normalizer = StringNormalizer(data_frame)
        data_frame = self.string_normalizer.normalize_string()

        self.missing_value_normalizer = MissingValue(data_frame)
        data_frame = self.missing_value_normalizer.normalize_missing_value()

        data_frame = data_frame.drop(['PTID'], axis=1)
        data_frame = data_frame.drop(['uvindex'], axis=1)

        print(data_frame.head())

        self.dataset_values = data_frame.values
        self.dataset_values = self.dataset_values.astype('float32')

        self.number_of_columns = number_of_columns
        self.predictor_column_no = self.number_of_columns - 1
        self.share_for_training = share_for_training


    def prepare_for_training(self):
        print(len(self.dataset_values[0]))

        dataset = self.scaler.fit_transform(self.dataset_values)

        train_size = int(len(dataset) * self.share_for_training)
        train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

        print(len(train), len(test))

        trainX, trainY = self.create_dataset(train, self.number_of_columns)
        testX, testY = self.create_dataset(test, self.number_of_columns)

        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY

        return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()


    def inverse_transform(self, train_predict, test_predict):
        train_predict = numpy.reshape(train_predict, (train_predict.shape[0], train_predict.shape[1]))
        test_predict = numpy.reshape(test_predict, (test_predict.shape[0], test_predict.shape[1]))

        self.trainX = numpy.reshape(self.trainX, (self.trainX.shape[0], self.trainX.shape[2]))
        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))

        trainXAndPredict = numpy.concatenate((self.trainX, train_predict),axis=1)
        testXAndPredict = numpy.concatenate((self.testX, test_predict),axis=1)

        trainY = numpy.reshape(self.trainY, (self.trainY.shape[0], 1))
        testY = numpy.reshape(self.testY, (self.testY.shape[0], 1))

        trainXAndY = numpy.concatenate((self.trainX, trainY),axis=1)
        testXAndY = numpy.concatenate((self.testX, testY),axis=1)

        trainXAndPredict = self.scaler.inverse_transform(trainXAndPredict)
        trainXAndY = self.scaler.inverse_transform(trainXAndY)

        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
        testXAndY = self.scaler.inverse_transform(testXAndY)

        train_predict = trainXAndPredict[:,self.predictor_column_no]
        trainY = trainXAndY[:,self.predictor_column_no]
        test_predict = testXAndPredict[:,self.predictor_column_no]
        testY = testXAndY[:,self.predictor_column_no]

        return train_predict, trainY, test_predict, testY


    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []

        for i in range(len(dataset) - 1):
            a = dataset[i, 0:look_back - 1]
            dataX.append(a)
            dataY.append(dataset[i, look_back - 1])

        return numpy.array(dataX), numpy.array(dataY)