from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui.tabs.wind_generator_tab.configuration import Configuration
from load_optimization.enum.generator_enum import GeneratorType
from load_optimization.generator_model.wind import WindGenerator

class WindGeneratorTab(Configuration):
    def __init__(self, tab: QWidget) -> None:
        super().__init__(tab)

    def get_wind_generator_model(self):
        #max and min power will be determine by wind speed
        max_power = 0
        min_power = 0
        cross_section = self.cross_sectional_aria_wind_spin_box.value()
        cut_in_speed = self.cut_in_speed_spin_box.value()
        cut_out_speed = self.cut_out_speed_spin_box.value()
        wind_generator_count = self.wind_generator_count_spin_box.value()

        wind_generator = WindGenerator(
            max_power,
            min_power,
            GeneratorType.WIND,
            cross_section,
            cut_in_speed,
            cut_out_speed,
            wind_generator_count
        )

        return wind_generator