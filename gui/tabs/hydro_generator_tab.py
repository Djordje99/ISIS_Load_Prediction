from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from load_optimization.generator.hydro import HydroGenerator
from load_optimization.generator_enum import GeneratorType

class HydroGeneratorTab():
    def __init__(self, tab:QWidget) -> None:
        self.max_hydro_power_spin_box = tab.findChild(QDoubleSpinBox, 'max_hydro_power_spin_box')
        self.min_hydro_power_spin_box = tab.findChild(QDoubleSpinBox, 'min_hydro_power_spin_box')
        self.hydro_generator_count_spin_box = tab.findChild(QSpinBox, 'hydro_generator_count_spin_box')


    def get_coal_generator_model(self):
        max_power = self.max_hydro_power_spin_box.value()
        min_power = self.min_hydro_power_spin_box.value()
        hydro_generator_count = self.hydro_generator_count_spin_box.value()

        hydro_generator = HydroGenerator(
            max_power,
            min_power,
            GeneratorType.HYDRO,
            hydro_generator_count
        )

        return hydro_generator


