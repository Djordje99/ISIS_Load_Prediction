from PyQt5.QtWidgets import QWidget

from gui.tabs.coal_generator_tab.graph_configuration import CoalTabGraphConfiguration
from load_optimization.generator_model.thermal import ThermalGenerator
from load_optimization.enum.generator_enum import GeneratorType


class CoalGeneratorTab(CoalTabGraphConfiguration):
    def __init__(self, tab:QWidget) -> None:
        super(CoalGeneratorTab, self).__init__(tab)
