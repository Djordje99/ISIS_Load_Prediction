from load_optimization.generator_model.generator import Generator

class HydroGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, fuel_price, hydro_co2_emission, count) -> None:
        super().__init__(max_production, min_production, generator_type, count)
        self._fuel_price = fuel_price
        self._hydro_co2_emission = hydro_co2_emission

    @property
    def fuel_price(self):
        return self._fuel_price

    @fuel_price.setter
    def fuel_price(self, value):
        self._fuel_price = value

    @property
    def hydro_co2_emission(self):
        return self._hydro_co2_emission

    @hydro_co2_emission.setter
    def hydro_co2_emission(self, value):
        self._hydro_co2_emission = value