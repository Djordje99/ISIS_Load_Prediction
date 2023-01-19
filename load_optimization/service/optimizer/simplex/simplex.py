from pulp import *
from statistics import mean
import numpy as np

from load_optimization.service.optimizer.simplex.graph_linearization import GraphLinearization

MAX_CO2_PRICE_PER_TON = 30

COAL_PERCENTAGE = 0.5
GAS_PERCENTAGE = 0.2
HYDRO_PERCENTAGE = 0.2
SOLAR_PERCENTAGE = 0.05
WIND_PERCENTAGE = 0.05


class Simplex():
    def __init__(self, cost_weight, co2_weight, cost_consumption_coal, cost_consumption_gas,
                coal_price, gas_price, hydro_price, #coal_power_range, gas_power_range,
                coal_co2_emission, gas_co2_emission, hydro_co2_emission,
                coal_co2_cost, gas_co2_cost,
                max_coal_consumption, max_gas_consumption,
                max_co2_coal_emission, max_co2_gas_emission,
                mean_load,
                coal_generator_count, gas_generator_count, hydro_generator_count, solar_generator_count, wind_generator_count) -> None:

        self.graph_linearization = GraphLinearization()

        self.problem = LpProblem("Simple LP Problem", LpMinimize)

        self.mean_load = mean_load

        self.coal_generator_count = coal_generator_count
        self.gas_generator_count = gas_generator_count
        self.hydro_generator_count = hydro_generator_count
        self.solar_generator_count = solar_generator_count
        self.wind_generator_count = wind_generator_count

        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        self.cost_consumption_coal = cost_consumption_coal
        self.cost_consumption_gas = cost_consumption_gas

        self.coal_price = coal_price
        self.gas_price = gas_price
        self.hydro_price = hydro_price

        self.coal_co2_emission = coal_co2_emission
        self.gas_co2_emission = gas_co2_emission
        self.hydro_co2_emission = hydro_co2_emission

        self.coal_co2_cost = coal_co2_cost
        self.gas_co2_cost = gas_co2_cost

        self.max_coal_consumption = max_coal_consumption
        self.max_gas_consumption = max_gas_consumption
        self.max_co2_coal_emission = max_co2_coal_emission
        self.max_co2_gas_emission = max_co2_gas_emission

    @property
    def generator_variables(self):
        return self._generator_variables

    @generator_variables.setter
    def generator_variables(self, value):
        self._generator_variables = value

        self.create_simplex_variable()

        self.create_objective_function()


    def get_coal_consumption_per_MW_function(self):
        a = 1
        b = 0

        if self.generator_variables.get('coal_0') is not None:
            coal_power = self.generator_variables['coal_0']
            a, b = self.graph_linearization.get_consumption_linear_approximation(self.cost_consumption_coal, self.mean_load,
                                                                                COAL_PERCENTAGE, coal_power[1], coal_power[0], self.coal_generator_count)

            a = a * self.max_gas_consumption

        return abs(a), b


    def get_gas_consumption_per_MW_function(self):
        a = 1
        b = 0

        if self.generator_variables.get('gas_0') is not None:
            gas_power = self.generator_variables['gas_0']
            a, b = self.graph_linearization.get_consumption_linear_approximation(self.cost_consumption_gas, self.mean_load,
                                                                                GAS_PERCENTAGE, gas_power[1], gas_power[0], self.gas_generator_count)

            a = a * self.max_gas_consumption

        return abs(a), b


    def get_coal_co2_emission_per_MW_function(self):
        a, b = np.polyfit([20, 100], [self.coal_co2_emission[0], self.coal_co2_emission[4]], 1)
        a = a * self.max_co2_coal_emission

        return abs(a)


    def get_gas_co2_emission_per_MW_function(self):
        a, b = np.polyfit([20, 100], [self.gas_co2_emission[0], self.gas_co2_emission[4]], 1)
        a = a * self.max_co2_gas_emission

        return abs(a)


    def get_coal_co2_price_per_ton_function(self):
        a, b = np.polyfit([20, 100], [self.coal_co2_emission[0], self.coal_co2_emission[4]], 1)
        a = a * MAX_CO2_PRICE_PER_TON

        return abs(a)


    def get_coal_co2_price_per_ton_function(self):
        a, b = np.polyfit([20, 100], [self.gas_co2_emission[0], self.gas_co2_emission[4]], 1)
        a = a * MAX_CO2_PRICE_PER_TON

        return abs(a)


    def create_simplex_variable(self):
        self.simplex_variable = {}
        for key, value in self._generator_variables.items():
            self.simplex_variable[key] = LpVariable(key, 0, value[1])


    def create_objective_function(self):
        objective_function = None

        coal_a, coal_b = self.get_coal_consumption_per_MW_function()
        gas_a, gas_b = self.get_gas_consumption_per_MW_function()

        coal_co2_emission = self.get_coal_co2_emission_per_MW_function()
        gas_co2_emission = self.get_gas_co2_emission_per_MW_function()

        coal_co2_price = self.get_coal_co2_price_per_ton_function()
        gas_co2_price = self.get_coal_co2_price_per_ton_function()

        for key, variable in self.simplex_variable.items():
            if 'coal' in key:
                objective_function += variable*(self.cost_weight*(coal_a*self.coal_price + coal_co2_emission*coal_co2_price) + self.co2_weight*(coal_co2_emission)) + self.cost_weight*coal_b
            if 'gas' in key:
                objective_function += variable*(self.cost_weight*(gas_a*self.gas_price + gas_co2_emission*gas_co2_price) + self.co2_weight*(gas_co2_emission)) + self.co2_weight*gas_b
            if 'hydro' in key:
                objective_function += variable*(self.cost_weight*(self.hydro_price + self.hydro_co2_emission*MAX_CO2_PRICE_PER_TON) + self.co2_weight*(self.hydro_co2_emission))

        self.problem += objective_function


    def create_constrain(self, load):
        self.problem.constraints.clear()

        expression = None

        for key, variable in self.simplex_variable.items():
            expression += variable

        constrain = LpConstraint(expression, sense = LpConstraintEQ, rhs = load)

        self.problem += constrain


    def optimization(self, load):
        is_running = True

        self.create_constrain(load)

        while(is_running):
            is_running = False
            self.problem.solve()

            for v in self.problem.variables():
                print(v.name, "=", v.varValue)
                if v.varValue != 0 and v.varValue < self.generator_variables[v.name][0]:
                    v.bounds(self.generator_variables[v.name][0], self.generator_variables[v.name][1])
                    is_running = True

        return self.get_generator_load_values(), self.get_generator_cost_values(), self.get_generator_co2_emission_values()


    def get_generator_load_values(self):
        generator_values = {}

        for variable in self.problem.variables():
            generator_values[variable.name] = variable.varValue

        generator_values = dict(sorted(generator_values.items()))

        return generator_values


    def get_generator_cost_values(self):
        generator_values = {}

        coal_a, coal_b = self.get_coal_consumption_per_MW_function()
        gas_a, gas_b = self.get_gas_consumption_per_MW_function()

        coal_co2_emission = self.get_coal_co2_emission_per_MW_function()
        gas_co2_emission = self.get_gas_co2_emission_per_MW_function()

        coal_co2_price = self.get_coal_co2_price_per_ton_function()
        gas_co2_price = self.get_coal_co2_price_per_ton_function()

        for variable in self.problem.variables():
            if 'coal' in variable.name:
                generator_values[variable.name] = variable.varValue*coal_a*self.coal_price + coal_b + variable.varValue*coal_co2_emission*coal_co2_price
            if 'gas' in variable.name:
                generator_values[variable.name] = variable.varValue*gas_a*self.gas_price + gas_b + variable.varValue*gas_co2_emission*gas_co2_price
            if 'hydro' in variable.name:
                generator_values[variable.name] = variable.varValue*(self.hydro_price + self.hydro_co2_emission*MAX_CO2_PRICE_PER_TON)

        generator_values = dict(sorted(generator_values.items()))

        return generator_values


    def get_generator_co2_emission_values(self):
        generator_values = {}

        coal_co2_emission = self.get_coal_co2_emission_per_MW_function()
        gas_co2_emission = self.get_gas_co2_emission_per_MW_function()

        for variable in self.problem.variables():
            if 'coal' in variable.name:
                generator_values[variable.name] = variable.varValue*coal_co2_emission
            if 'gas' in variable.name:
                generator_values[variable.name] = variable.varValue*gas_co2_emission
            if 'hydro' in variable.name:
                generator_values[variable.name] = variable.varValue*self.hydro_co2_emission

        generator_values = dict(sorted(generator_values.items()))

        return generator_values