from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from load_optimization.generator_model.hydro import HydroGenerator
from load_optimization.enum.generator_enum import GeneratorType

class HydroGeneratorTab():
    def __init__(self, tab:QWidget) -> None:
        self.max_hydro_power_spin_box = tab.findChild(QDoubleSpinBox, 'max_hydro_power_spin_box')
        self.min_hydro_power_spin_box = tab.findChild(QDoubleSpinBox, 'min_hydro_power_spin_box')
        self.hydro_generator_count_spin_box = tab.findChild(QSpinBox, 'hydro_generator_count_spin_box')
        self.hydro_cost_spin_box = tab.findChild(QDoubleSpinBox, 'hydro_cost_spin_box')
        self.hydro_co2_emission_spin_box = tab.findChild(QDoubleSpinBox, 'hydro_co2_emission_spin_box')


    def get_hydro_generator_model(self):
        max_power = self.max_hydro_power_spin_box.value()
        min_power = self.min_hydro_power_spin_box.value()
        hydro_generator_count = self.hydro_generator_count_spin_box.value()
        hydro_cost = self.hydro_cost_spin_box.value()
        hydro_co2_emission = self.hydro_co2_emission_spin_box.value()

        hydro_generator = HydroGenerator(
            max_power,
            min_power,
            GeneratorType.HYDRO,
            hydro_generator_count,
            hydro_cost,
            hydro_co2_emission
        )

        return hydro_generator


