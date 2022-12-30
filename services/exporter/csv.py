from database.controller import DatabaseController

FILE_PATH = 'D:\\Fax\\ISIS_Load_Prediction\\predicted_data.csv'

class CsvExporter():
    def __init__(self) -> None:
        self.controller = DatabaseController()


    def export(self):
        data_frame = self.controller.load_predicted_load()

        data_frame.to_csv(FILE_PATH, index=False)