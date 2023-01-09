from load_optimization.generator.generator import Generator

class SolarGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, panel_size, efficiency, count) -> None:
        super().__init__(max_production, min_production, generator_type, count)
        self._panel_size = panel_size
        self._efficiency = efficiency


    @property
    def panel_size(self):
        return self._panel_size

    @panel_size.setter
    def panel_size(self, value):
        self._panel_size = value

    @property
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = value
