from pulp import *
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from statistics import mean

FUNCTION_RANGE = [0, 20, 40, 60, 80, 100]
MAX_COAL_CONSUMPTION = 0.9 / 100
MAX_GAS_CONSUMPTION = 0.3 / 100

MAX_COAL_CO2_EMISSION = 40
MAX_GAS_CO2_EMISSION = 20

MAX_CO2_PRICE_PER_TON = 30


class Simplex():
    def __init__(self, cost_weight, co2_weight, cost_consumption_coal, cost_consumption_gas,
                coal_price, gas_price, hydro_price, #coal_power_range, gas_power_range,
                coal_co2_emission, gas_co2_emission, hydro_co2_emission, coal_co2_cost, gas_co2_cost) -> None:

        self.problem = LpProblem("Simple LP Problem", LpMinimize)

        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        self.cost_consumption_coal = cost_consumption_coal
        self.cost_consumption_gas = cost_consumption_gas

        self.coal_price = coal_price
        self.gas_price = gas_price
        self.hydro_price = hydro_price

        # self.coal_power_range = coal_power_range
        # self.gas_power_range = gas_power_range

        self.coal_co2_emission = coal_co2_emission
        self.gas_co2_emission = gas_co2_emission
        self.hydro_co2_emission = hydro_co2_emission

        self.coal_co2_cost = coal_co2_cost
        self.gas_co2_cost = gas_co2_cost

    @property
    def generator_variables(self):
        return self._generator_variables

    @generator_variables.setter
    def generator_variables(self, value):
        self._generator_variables = value

        # Create problem variables
        self.create_simplex_variable()

        # The objective function is added to 'prob' first
        self.create_objective_function()


    def get_coal_consumption_per_MW_function(self):
        # x1 = self.coal_power_range[0]
        # x2 = self.coal_power_range[len(self.coal_power_range) - 1]

        # y1 = self.cost_consumption_coal[0] * MAX_COAL_CONSUMPTION
        # y2 = self.cost_consumption_coal[len(self.cost_consumption_coal) - 1] * MAX_COAL_CONSUMPTION

        # m = (y2 - y1) / (x2 - x1)

        m = mean(self.cost_consumption_coal) * MAX_COAL_CONSUMPTION

        return m


    def get_gas_consumption_per_MW_function(self):
        # x1 = self.gas_power_range[0]
        # x2 = self.gas_power_range[len(self.gas_power_range) - 1]

        # y1 = self.cost_consumption_gas[0] * MAX_GAS_CONSUMPTION
        # y2 = self.cost_consumption_gas[len(self.cost_consumption_gas) - 1] * MAX_GAS_CONSUMPTION

        # m = (y2 - y1) / (x2 - x1)

        m = mean(self.cost_consumption_gas) * MAX_GAS_CONSUMPTION

        return m


    def get_coal_co2_emission_per_MW_function(self):
        m = mean(self.coal_co2_emission) * MAX_COAL_CO2_EMISSION

        return m


    def get_gas_co2_emission_per_MW_function(self):
        m = mean(self.gas_co2_emission) * MAX_GAS_CO2_EMISSION

        return m


    def get_coal_co2_price_per_ton_function(self):
        m = mean(self.coal_co2_emission) * MAX_CO2_PRICE_PER_TON

        return m


    def get_coal_co2_price_per_ton_function(self):
        m = mean(self.gas_co2_emission) * MAX_CO2_PRICE_PER_TON

        return m


    def create_simplex_variable(self):
        self.simplex_variable = {}
        for key, value in self._generator_variables.items():
            self.simplex_variable[key] = LpVariable(key, 0, value[1])


    def create_objective_function(self):
        objective_function = None

        coal_m = self.get_coal_consumption_per_MW_function()
        gas_m = self.get_gas_consumption_per_MW_function()

        coal_co2_emission = self.get_coal_co2_emission_per_MW_function()
        gas_co2_emission = self.get_gas_co2_emission_per_MW_function()

        coal_co2_price = self.get_coal_co2_price_per_ton_function()
        gas_co2_price = self.get_coal_co2_price_per_ton_function()

        for key, variable in self.simplex_variable.items():
            if 'coal' in key:
                objective_function += variable*(self.cost_weight*(coal_m*self.coal_price + coal_co2_emission*coal_co2_price) + self.co2_weight*(coal_co2_emission))
            if 'gas' in key:
                objective_function += variable*(self.cost_weight*(gas_m*self.gas_price + gas_co2_emission*gas_co2_price) + self.co2_weight*(gas_co2_emission))
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

        # The constraints are added to 'prob' one at a time
        self.create_constrain(load)

        while(is_running):
            is_running = False
            # The problem is solved using PuLP's choice of Solver
            self.problem.solve()

            # The status of the solution is printed to the screen
            print("Status:", LpStatus[self.problem.status])

            # Each of the variables is printed with it's resolved optimum value
            for v in self.problem.variables():
                print(v.name, "=", v.varValue)
                if v.varValue != 0 and v.varValue < self.generator_variables[v.name][0]:
                    v.bounds(self.generator_variables[v.name][0], self.generator_variables[v.name][1])
                    is_running = True

        # The optimised objective function value is printed to the screen
        print("objective_function = ", value(self.problem.objective))

        return self.get_generator_values()


    def get_generator_values(self):
        generator_values = {}

        for variable in self.problem.variables():
            generator_values[variable.name] = variable.varValue

        generator_values = dict(sorted(generator_values.items()))

        return generator_values