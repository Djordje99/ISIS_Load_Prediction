from load_optimization.generator_model.generator import Generator

class HydroGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type) -> None:
        super().__init__(max_production, min_production, generator_type)
