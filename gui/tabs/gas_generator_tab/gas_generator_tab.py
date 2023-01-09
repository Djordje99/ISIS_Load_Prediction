from gui.tabs.gas_generator_tab.graph_configuration import GasTabGraphConfiguration
from load_optimization.generator.thermal import ThermalGenerator
from load_optimization.generator_enum import GeneratorType

class GasGeneratorTab(GasTabGraphConfiguration):
    def __init__(self, tab) -> None:
        super(GasGeneratorTab, self).__init__(tab)


    def get_gas_generator_model(self):
        gas_consumption = self.get_gas_consumption_slider_value()
        co2_emission = self.get_gas_co2_emission_slider_value()
        max_power = self.max_thermal_gas_power_spin_box.value()
        min_power = self.min_thermal_gas_power_spin_box.value()
        gas_cost = self.gas_cost_spin_box.value()
        power_plant_count = self.thermal_gas_count_spin_box.value()

        #Crate model
        thermal_gas_generator = ThermalGenerator(
            max_power,
            min_power,
            GeneratorType.THERMAL_GAS,
            power_plant_count,
            co2_emission,
            gas_consumption,
            gas_cost
        )

        return thermal_gas_generator