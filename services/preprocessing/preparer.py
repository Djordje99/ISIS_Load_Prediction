import numpy
from sklearn.preprocessing import MinMaxScaler
from database.controller import DatabaseController


class Preparer:
    def __init__(self, share_for_training):
        self.share_for_training = share_for_training
        self.controller = DatabaseController()

        self.scaler = MinMaxScaler(feature_range=(0, 1))


    def prepare_predict_date(self, from_date, to_date):
        data_frame = self.controller.get_data_frame_from_date(from_date, to_date)

        self.number_of_columns = len(data_frame.columns)
        self.predictor_column_no = self.number_of_columns - 1

        print(len(data_frame.columns))

        predict_dataset_values = data_frame.values
        predict_dataset_values = predict_dataset_values.astype('float32')

        dataset = self.scaler.fit_transform(predict_dataset_values)

        X_test, y_test = self.create_dataset(dataset, len(data_frame.columns))

        X_test = numpy.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        self.testX = X_test
        self.testY = y_test

        return X_test.copy(), y_test.copy()



    def prepare_data_frame(self, selected_features=''):
        self.controller = DatabaseController()
        self.data_frame = self.controller.load_data()
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        # self.selector = FeatureSelectionRFE()
        # self.data_frame = self.selector.select_features(self.data_frame, 20)

        if len(selected_features) > 0:
            selected_features += '1'
            self.data_frame = self.data_frame.loc[:, [True if selected_features[i] == '1' else False for i in range(len(selected_features))]]

        self.dataset_values = self.data_frame.values
        self.dataset_values = self.dataset_values.astype('float32')

        self.number_of_columns = len(self.data_frame.columns)
        self.predictor_column_no = self.number_of_columns - 1


    def get_prepared_data_frame(self):
        return self.data_frame


    def prepare_for_training(self, selected_features=[]):
        self.prepare_data_frame(selected_features)

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


    def inverse_predict_transform(self, test_predict):
        test_predict = numpy.reshape(test_predict, (test_predict.shape[0], test_predict.shape[1]))

        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))

        testXAndPredict = numpy.concatenate((self.testX, test_predict),axis=1)

        y_test = numpy.reshape(self.testY, (self.testY.shape[0], 1))

        testXAndY = numpy.concatenate((self.testX, y_test),axis=1)

        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
        testXAndY = self.scaler.inverse_transform(testXAndY)

        test_predict = testXAndPredict[:,self.predictor_column_no]
        y_test = testXAndY[:,self.predictor_column_no]

        return test_predict, y_test


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
