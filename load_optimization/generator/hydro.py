from load_optimization.generator.generator import Generator

class HydroGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, count, fuel_price) -> None:
        super().__init__(max_production, min_production, generator_type, count)
        self._fuel_price = fuel_price


    @property
    def fuel_price(self):
        return self._fuel_price

    @fuel_price.setter
    def fuel_price(self, value):
        self._fuel_price = value