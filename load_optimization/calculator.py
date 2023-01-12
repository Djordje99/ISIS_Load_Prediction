from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from database.controller import DatabaseController
from load_optimization.symplex import Simplex
from load_optimization.generator.thermal import ThermalGenerator
from load_optimization.generator.hydro import HydroGenerator
from load_optimization.generator.wind import WindGenerator
from load_optimization.generator.solar import SolarGenerator

AIR_DENSITY = 1.225

class Calculator():
    def __init__(self, coal_generator:ThermalGenerator, gas_generator:ThermalGenerator, hydro_generator:HydroGenerator,
                    solar_generator:SolarGenerator, wind_generator:WindGenerator,  cost_weight, co2_weight) -> None:
        self.database_controller = DatabaseController()
        self.simplex = Simplex()
        self.coal_generator = coal_generator
        self.gas_generator = gas_generator
        self.hydro_generator = hydro_generator
        self.solar_generator = solar_generator
        self.wind_generator = wind_generator
        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        self.predicted_load_df = self.__load_predicted_load()
        self.weather_data = self.__load_weather_data(self.predicted_load_df['date'].min())

        self.wind_power_output = self.get_wind_generator_power_output()
        self.solar_power_output = self.get_solar_generator_power_output()


    def __load_predicted_load(self):
        predicted_load_df = self.database_controller.load_predicted_load()

        return predicted_load_df


    def __load_weather_data(self, date_min:str):
        weather_data_df = None

        date_max = date_min.split(' ')[0] + '23:00:00'

        date = QDateTime.fromString(date_min, 'yyyy-MM-dd hh:mm:ss')
        date_border = QDateTime(2021, 9, 7, 0, 0)

        if (date < date_border):
            weather_data_df = self.database_controller.load_training_data(date_min, date_max)
        else:
            weather_data_df = self.database_controller.load_test_data(date_min, date_max)

        return weather_data_df


    def call_simplex(self):
        c = self.create_objective_function()
        A_eq = [[1 for i in range(0, len(c))]]
        integrality = [2 for i in range(0, len(c))]
        bounds = []
        results = []

        for i in range(0, self.coal_generator.count):
            bounds.append((self.coal_generator.min_production, self.coal_generator.max_production))

        for i in range(0, self.gas_generator.count):
            bounds.append((self.gas_generator.min_production, self.gas_generator.max_production))

        for i in range(0, self.hydro_generator.count):
            bounds.append((self.hydro_generator.min_production, self.hydro_generator.max_production))

        for i in range(0, 24):
            b_eq = [self.predicted_load_df['predicted_load'][i] - self.solar_power_output[i] - self.wind_power_output[i]]

            result = self.simplex.optimize(A_eq=A_eq, b_eq=b_eq, bounds=bounds, c=c, integrality=integrality)

            results.append(result)

        return results


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


    def get_wind_generator_power_output(self):
        hourly_power = []

        for wind_speed in self.weather_data['windspeed']:
            if wind_speed >= self.wind_generator.cut_out_speed or wind_speed <= self.wind_generator.cut_in_speed:
                hourly_power.append(0)
            else:
                power = (1/2) * AIR_DENSITY * self.wind_generator.cross_section * pow(wind_speed, 3) * self.wind_generator.count
                power = power / 1000000
                hourly_power.append(power)

        return hourly_power


    def get_solar_generator_power_output(self):
        hourly_power = []

        for solar_radiation in self.weather_data['solarradiation']:
            power = self.solar_generator.panel_size * self.solar_generator.efficiency * solar_radiation * self.solar_generator.count
            power = power / 1000000
            hourly_power.append(power)

        return hourly_power