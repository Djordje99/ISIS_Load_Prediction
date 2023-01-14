from pulp import *
from scipy.interpolate import interp1d


FUNCTION_RANGE = [0, 20, 40, 60, 80, 100]
MAX_COAL_CONSUMPTION = 0.9 / 100
MAX_GAS_CONSUMPTION = 0.03 / 100


class Simplex():
    def __init__(self, cost_weight, co2_weight, cost_consumption_coal, cost_consumption_gas, coal_price, gas_price, coal_power_range, gas_power_range) -> None:
        self.problem = LpProblem("Simple LP Problem", LpMinimize)

        self.cost_weight = cost_weight
        self.co2_weight = co2_weight

        self.cost_consumption_coal = cost_consumption_coal.insert(0,0)
        self.cost_consumption_gas = cost_consumption_gas.insert(0,0)

        self.coal_price = coal_price
        self.gas_price = gas_price

        self.coal_power_range = coal_power_range
        self.gas_power_range = gas_power_range


    def get_coal_consumption_per_MW_function(self, x):
        if x is None:
            return 0

        fun = interp1d(self.coal_power_range, self.cost_consumption_coal * MAX_COAL_CONSUMPTION , kind='linear')
        value = fun(x)

        return value


    def get_gas_consumption_per_MW_function(self, x):
        if x is None:
            return 0

        fun = interp1d(self.gas_power_range, self.cost_consumption_gas * MAX_GAS_CONSUMPTION, kind='linear')
        value = fun(x)

        return value


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


    def create_simplex_variable(self):
        self.simplex_variable = {}
        for key, value in self._generator_variables.items():
            self.simplex_variable[key] = LpVariable(key, 0, value[1])


    def create_objective_function(self):
        objective_function = None

        for key, variable in self.simplex_variable.items():
            if 'coal' in key:
                objective_function += variable*self.get_coal_consumption_per_MW_function(variable.varValue)*self.coal_price + 300*variable
            if 'gas' in key:
                objective_function += variable*self.get_gas_consumption_per_MW_function(variable.varValue)*self.gas_price + 240*variable
            if 'hydro' in key:
                objective_function += (20 + 30)*variable

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