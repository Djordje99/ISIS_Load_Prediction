from sklearn.preprocessing import LabelEncoder

STRING_FEATURES = ['conditions']

class StringNormalizer():
    def __init__(self, data_frame) -> None:
        self.data_frame = data_frame
        self.label_encoder = LabelEncoder()


    def normalize_string(self):
        for feature in STRING_FEATURES:
            self.data_frame[feature] = self.label_encoder.fit_transform(self.data_frame[feature])

        return self.data_frame