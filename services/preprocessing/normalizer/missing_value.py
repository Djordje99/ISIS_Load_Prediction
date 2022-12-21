
MISSING_VALUE_BORDER = 0

class MissingValue():
    def __init__(self, data_frame) -> None:
        self.data_frame = data_frame


    def normalize_missing_value(self):
        ratios = [ratio for ratio in (self.data_frame.isna().sum()/len(self.data_frame))]

        for pair in list(zip(self.data_frame.columns, ratios)):
            if pair[1] > MISSING_VALUE_BORDER:
                self.data_frame = self.data_frame.drop([pair[0]], axis=1)

        return self.data_frame