from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class FeatureSelectionRFE():
    def __init__(self) -> None:
        pass

    def select_features(self, data_frame, n_features_to_select):
        model = LinearRegression()

        rfe = RFE(model, n_features_to_select=n_features_to_select)

        y = data_frame['load']
        X = data_frame.drop('load', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9, random_state=42)

        X_selected = rfe.fit_transform(X_train, y_train)

        feature_mask = rfe.support_

        data_frame = data_frame.drop('load', axis=1).loc[:, feature_mask]

        print(data_frame.head())

        return data_frame