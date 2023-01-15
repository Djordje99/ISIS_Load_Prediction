from load_optimization.generator_model.generator import Generator

class WindGenerator(Generator):
    def __init__(self, max_production, min_production, generator_type, cross_section, cut_in_speed, cut_out_speed) -> None:
        super().__init__(max_production, min_production, generator_type)
        self._cross_section = cross_section
        self._cut_in_speed = cut_in_speed
        self._cut_out_speed = cut_out_speed


    @property
    def cross_section(self):
        return self._cross_section

    @cross_section.setter
    def cross_section(self, value):
        self._cross_section = value

    @property
    def cut_in_speed(self):
        return self._cut_in_speed

    @cut_in_speed.setter
    def cut_in_speed(self, value):
        self._cut_in_speed = value

    @property
    def cut_out_speed(self):
        return self._cut_out_speed

    @cut_out_speed.setter
    def cut_out_speed(self, value):
        self._cut_out_speed = value