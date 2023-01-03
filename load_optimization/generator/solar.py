from load_optimization.generator.generator import Generator

class SolarGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, count) -> None:
        super().__init__(max_production, min_production, generator_type, count)
