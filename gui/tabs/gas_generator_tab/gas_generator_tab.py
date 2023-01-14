from gui.tabs.gas_generator_tab.graph_configuration import GasTabGraphConfiguration
from load_optimization.generator_model.thermal import ThermalGenerator
from load_optimization.enum.generator_enum import GeneratorType

class GasGeneratorTab(GasTabGraphConfiguration):
    def __init__(self, tab) -> None:
        super(GasGeneratorTab, self).__init__(tab)
