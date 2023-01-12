from database.controller import DatabaseController
from load_optimization.generator.thermal import ThermalGenerator
from load_optimization.generator.hydro import HydroGenerator


class Calculator():
    def __init__(self, coal_generator:ThermalGenerator, gas_generator:ThermalGenerator, hydro_generator:HydroGenerator,
                    solar_generator, wind_generator,  cost_weight, co2_weight) -> None:
        self.database_controller = DatabaseController()

        self.coal_generator = coal_generator
        self.gas_generator = gas_generator
        self.hydro_generator = hydro_generator
        self.solar_generator = solar_generator
        self.wind_generator = wind_generator
        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        self.predicted_load_df = self.__load_predicted_load()


    def __load_predicted_load(self):
        predicted_load_df = self.database_controller.load_predicted_load()

        return predicted_load_df


    def call_simplex(self):
        c = self.create_objective_function()
        print(c)


    def create_objective_function(self):
        c = []
        c_coal = self.get_objective_function_coal()
        c_gas = self.get_objective_function_gas()
        c_hydro = self.get_objective_function_hydro()

        c.extend(c_coal)
        c.extend(c_gas)
        c.extend(c_hydro)

        return c


    def get_objective_function_coal(self):
        c_coal = []

        for i in range(0, self.coal_generator.count):
            c_coal.append(self.co2_weight*self.coal_generator.co2_emission_values[3] + self.cost_weight*self.coal_generator.fuel_price)

        return c_coal


    def get_objective_function_gas(self):
        c_gas = []

        for i in range(0, self.gas_generator.count):
            c_gas.append(self.co2_weight*self.gas_generator.co2_emission_values[3] + self.cost_weight*self.gas_generator.fuel_price)

        return c_gas


    def get_objective_function_hydro(self):
        c_hydro = []

        for i in range(0, self.hydro_generator.count):
            c_hydro.append(self.co2_weight*self.hydro_generator.hydro_co2_emission + self.cost_weight*self.hydro_generator.fuel_price)

        return c_hydro
