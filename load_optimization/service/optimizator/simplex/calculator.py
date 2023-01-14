from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from database.controller import DatabaseController
from load_optimization.service.optimizator.simplex.simplex import Simplex
from load_optimization.generator_model.thermal import ThermalGenerator
from load_optimization.generator_model.hydro import HydroGenerator
from load_optimization.generator_model.wind import WindGenerator
from load_optimization.generator_model.solar import SolarGenerator

from pulp import *

import numpy as np


AIR_DENSITY = 1.225


class Calculator():
    def __init__(self, coal_generator:ThermalGenerator, gas_generator:ThermalGenerator, hydro_generator:HydroGenerator,
                    solar_generator:SolarGenerator, wind_generator:WindGenerator,  cost_weight, co2_weight) -> None:
        self.database_controller = DatabaseController()
        self.coal_generator = coal_generator
        self.gas_generator = gas_generator
        self.hydro_generator = hydro_generator
        self.solar_generator = solar_generator
        self.wind_generator = wind_generator
        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        # COAL_POWER_RANGE = [i for i in np.linspace(self.coal_generator.min_production,
        #                                     self.coal_generator.max_production, 6)]

        # GAS_POWER_RANGE = [i for i in np.linspace(self.gas_generator.min_production,
        #                                     self.gas_generator.max_production, 6)]

        self.simplex = Simplex(cost_weight, co2_weight, self.coal_generator.consumption_values, self.gas_generator.consumption_values,
                                self.coal_generator.fuel_price, self.gas_generator.fuel_price, self.hydro_generator.fuel_price, #COAL_POWER_RANGE, GAS_POWER_RANGE,
                                self.coal_generator.co2_emission_values, self.gas_generator.co2_emission_values, self.hydro_generator.hydro_co2_emission,
                                self.coal_generator.co2_price_values, self.gas_generator.co2_price_values)

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
        x_variables = self.create_generator_variable()
        self.simplex.generator_variables = x_variables
        results = {}

        for hour in range(0, 24):
            predicted_load_hourly = self.predicted_load_df['predicted_load'][hour] - self.solar_power_output[hour] - self.wind_power_output[hour]

            result = self.simplex.optimization(predicted_load_hourly)
            results[hour] = result


        return results


    def create_generator_variable(self):
        x = {}
        x_coal = self.get_coal_variable()
        x_gas = self.get_gas_variable()
        x_hydro = self.get_hydro_variable()

        x.update(x_coal)
        x.update(x_gas)
        x.update(x_hydro)

        return x


    def get_coal_variable(self):
        x_coal = {}

        for i in range(0, self.coal_generator.count):
            x_coal[f'coal_{i}'] = (self.coal_generator.min_production, self.coal_generator.max_production)

        return x_coal


    def get_gas_variable(self):
        x_gas = {}

        for i in range(0, self.gas_generator.count):
            x_gas[f'gas_{i}'] = (self.gas_generator.min_production, self.gas_generator.max_production)

        return x_gas


    def get_hydro_variable(self):
        x_hydro = {}

        for i in range(0, self.hydro_generator.count):
            x_hydro[f'hydro_{i}'] = (self.hydro_generator.min_production, self.hydro_generator.max_production)

        return x_hydro


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