from database.controller import DatabaseController

class Calculator():
    def __init__(self, coal_generator, gas_generator, hydro_generator, solar_generator, wind_generator) -> None:
        self.coal_generator = coal_generator
        self.gas_generator = gas_generator
        self.hydro_generator = hydro_generator
        self.solar_generator = solar_generator
        self.wind_generator = wind_generator

        self.predicted_load_df = self.__load_predicted_load()

        self.database_controller = DatabaseController()


    def __load_predicted_load(self):
        predicted_load_df = self.database_controller.load_predicted_load()

        return predicted_load_df
