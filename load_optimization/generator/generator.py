RANGE = [20, 40, 60, 80, 100]

class Generator():
    def __init__(self, max_production, min_production, generator_type, count) -> None:
        self._max_production = max_production
        self._min_production = min_production
        self._generator_type = generator_type
        self.count = count

    @property
    def max_production(self):
        return self._max_production

    @max_production.setter
    def max_production(self, value):
        self._max_production = value

    @property
    def min_production(self):
        return self._min_production

    @min_production.setter
    def min_production(self, value):
        self._min_production = value

    @property
    def generator_type(self):
        return self._generator_type

    @generator_type.setter
    def generator_type(self, value):
        self._generator_type = value

    @property
    def count(self):
        return self.count

    @count.setter
    def count(self, value):
        self.count = value
