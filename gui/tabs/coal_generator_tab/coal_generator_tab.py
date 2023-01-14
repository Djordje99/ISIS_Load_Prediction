from PyQt5.QtWidgets import QWidget

from gui.tabs.coal_generator_tab.graph_configuration import CoalTabGraphConfiguration
from load_optimization.generator_model.thermal import ThermalGenerator
from load_optimization.enum.generator_enum import GeneratorType


class CoalGeneratorTab(CoalTabGraphConfiguration):
    def __init__(self, tab:QWidget) -> None:
        super(CoalGeneratorTab, self).__init__(tab)


    def get_coal_generator_model(self):
        coal_consumption = self.get_coal_consumption_slider_value()
        co2_emission = self.get_coal_co2_emission_slider_value()
        max_power = self.max_thermal_coal_power_spin_box.value()
        min_power = self.min_thermal_coal_power_spin_box.value()
        coal_cost = self.coal_cost_spin_box.value()
        power_plant_count = self.thermal_coal_count_spin_box.value()

        #Crate model
        thermal_coal_generator = ThermalGenerator(
            max_power,
            min_power,
            GeneratorType.THERMAL_COAL,
            power_plant_count,
            co2_emission,
            coal_consumption,
            coal_cost
        )

        return thermal_coal_generator


