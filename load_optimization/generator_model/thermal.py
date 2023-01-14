from load_optimization.generator_model.generator import Generator

class ThermalGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, fuel_price, max_fuel_consumption, max_co2_emission, count) -> None:
        super().__init__(max_production, min_production, generator_type, count)
        self._fuel_price = fuel_price
        self._max_fuel_consumption = max_fuel_consumption
        self._max_co2_emission = max_co2_emission


    @property
    def fuel_price(self):
        return self._fuel_price

    @fuel_price.setter
    def fuel_price(self, value):
        self._fuel_price = value

    @property
    def max_fuel_consumption(self):
        return self._max_fuel_consumption

    @max_fuel_consumption.setter
    def max_fuel_consumption(self, value):
        self._max_fuel_consumption = value

    @property
    def max_co2_emission(self):
        return self._max_co2_emission

    @max_co2_emission.setter
    def max_co2_emission(self, value):
        self._max_co2_emission = value