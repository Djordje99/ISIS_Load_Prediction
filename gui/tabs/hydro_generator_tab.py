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
