from gui.tabs.coal_generator_tab.graph_configuration import CoalTabGraphConfiguration


class CoalGeneratorTab(CoalTabGraphConfiguration):
    def __init__(self, window) -> None:
        super(CoalGeneratorTab, self).__init__(window)


    def get_coal_generator_data(self):
        coal_consumption = self.get_coal_consumption_slider_value()
        co2_emission = self.get_coal_co2_emission_slider_value()
        max_power = self.window.max_thermal_coal_power_spin_box.value()
        min_power = self.window.min_thermal_coal_power_spin_box.value()
        coal_cost = self.window.coal_cost_spin_box.value()
        power_plant_count = self.window.thermal_coal_count_spin_box.value()

        return max_power, min_power, coal_cost, power_plant_count, coal_consumption, co2_emission


