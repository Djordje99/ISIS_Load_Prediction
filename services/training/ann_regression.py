from keras.layers import Dense
from keras.models import Sequential
from tensorflow import keras
from services.training.ann_base import AnnBase
import os


MODEL_NAME = 'model\\previous_load_model'
MODEL_PATH =  os.path.dirname(__file__)


class AnnRegression(AnnBase):
    def get_model(self, size_shape):
        model = Sequential()

        if self.number_of_hidden_layers > 0:
            model.add(Dense(self._number_of_neurons_in_first_hidden_layer, input_shape=(1, size_shape), kernel_initializer=self.kernel_initializer, activation=self.activation_function))
            if self.number_of_hidden_layers > 1:
                for i in range(self.number_of_hidden_layers - 1):
                    model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer=self.kernel_initializer, activation=self.activation_function))

        model.add(Dense(self.number_of_neurons_in_second_hidden_layer, kernel_initializer=self.kernel_initializer, activation=self.activation_function))
        model.add(Dense(1, kernel_initializer=self.kernel_initializer))

        return model


    def get_model_from_path(self, path):
        model = keras.models.load_model(path)
        return model


    def compile_and_fit(self, trainX, trainY, size_shape):
        self.model = self.get_model(size_shape)
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.trainX = trainX

        self.model.fit(trainX, trainY, epochs=self.epoch_number, batch_size=self.batch_size_number, verbose=self.verbose)

        self.model.save(f'{MODEL_PATH}\\{MODEL_NAME}')


    def use_current_model(self, path, trainX):
        self.trainX = trainX
        self.model = self.get_model_from_path(path)


    def get_predict(self, testX):
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(testX)
        return trainPredict, testPredict


    def compile_fit_predict(self, trainX, trainY, testX, size_shape):
        self.compile_and_fit(trainX, trainY, size_shape)
        #self.use_current_model(f'{MODEL_PATH}\\{MODEL_NAME}', trainX)
        return self.get_predict(testX)
