from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from database.controller import DatabaseController
from services.preprocessing.preparer import Preparer

TRAINING_SHARE = 0.85

class ForwardFeatureSelection:
    def __init__(self) -> None:
        self.database_controller = DatabaseController()
        self.preparer = Preparer(TRAINING_SHARE)
        self.data_frame = self.database_controller.load_data()
        self.feature_number = len(self.data_frame.columns) - 1
        self.selected_features = ''
        self.features_and_error = []


    def create_feature_combination(self):
        combinations = []
        for combination_num in range(self.feature_number):
            combination = self.selected_features
            for i in range(self.feature_number - len(self.select_features)):
                if i == combination_num + len(self.select_features):
                    combination += '1'
                else:
                    combination += '0'

            combinations.append(combination)

        return combinations



    def select_features(self):
        X_train, y_train, X_test, y_test = self.preparer.prepare_for_training()

        for feature in X.columns:
            # Create a copy of the current list of selected features
            temp_selected_features = selected_features.copy()
            # Add the current feature to the list
            temp_selected_features.append(feature)
            # Extract the features from the training and test sets
            X_train_temp = X_train[temp_selected_features]
            X_test_temp = X_test[temp_selected_features]
            # Train a linear regression model using the current set of features
            model = LinearRegression()
            model.fit(X_train_temp, y_train)
            # Evaluate the model performance on the test set
            y_pred = model.predict(X_test_temp)
            mse = mean_squared_error(y_test, y_pred)
            # If the performance improves with the addition of the feature, add it to the list of selected features
            if mse < min_mse:
                selected_features = temp_selected_features
                min_mse = mse
            # Stop the iteration if the stopping criterion is reached
            if len(selected_features) == max_features:
                break

        # Print the list of selected features
        print(selected_features)