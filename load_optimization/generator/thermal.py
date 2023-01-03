from load_optimization.generator.generator import Generator

class ThermalGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, count, co2_emission_values, consumption_values, fuel_price) -> None:
        super().__init__(max_production, min_production, generator_type, count)
        self.co2_emission_values = co2_emission_values
        self.consumption_values = consumption_values
        self.fuel_price = fuel_price


    @property
    def co2_emission_values(self):
        return self.co2_emission_values

    @co2_emission_values.setter
    def co2_emission_values(self, value):
        self.co2_emission_values = value

    @property
    def consumption_values(self):
        return self.consumption_values

    @consumption_values.setter
    def consumption_values(self, value):
        self.consumption_values = value

    @property
    def fuel_price(self):
        return self.fuel_price

    @fuel_price.setter
    def fuel_price(self, value):
        self.fuel_price = value