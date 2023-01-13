from PyQt5.QtWidgets import QWidget

from gui.tabs.coal_generator_tab.slider_graph_update import CoalTabSliderGraphUpdate

FUEL_COST_DEFAULT = [20, 40, 65, 80, 100]
EMISSION_DEFAULT = [40, 20, 45, 75, 100]
CO2_COST_DEFAULT = [60, 40, 30, 70, 100]

class CoalTabSliderConfiguration(CoalTabSliderGraphUpdate):
    def __init__(self, tab:QWidget) -> None:
        super().__init__(tab)
        self.configure_sliders()


    def configure_sliders(self):
        self.configure_co2_coal_sliders()
        self.configure_consumption_coal_sliders()
        self.configure_co2_cost_coal_sliders()


    def configure_co2_coal_sliders(self):
        self.thermal_coal_slider_1.setValue(EMISSION_DEFAULT[0])
        self.thermal_coal_slider_2.setValue(EMISSION_DEFAULT[1])
        self.thermal_coal_slider_3.setValue(EMISSION_DEFAULT[2])
        self.thermal_coal_slider_4.setValue(EMISSION_DEFAULT[3])
        self.thermal_coal_slider_5.setValue(EMISSION_DEFAULT[4])


    def configure_co2_cost_coal_sliders(self):
        self.thermal_coal_co2_cost_slider_1.setValue(CO2_COST_DEFAULT[0])
        self.thermal_coal_co2_cost_slider_2.setValue(CO2_COST_DEFAULT[1])
        self.thermal_coal_co2_cost_slider_3.setValue(CO2_COST_DEFAULT[2])
        self.thermal_coal_co2_cost_slider_4.setValue(CO2_COST_DEFAULT[3])
        self.thermal_coal_co2_cost_slider_5.setValue(CO2_COST_DEFAULT[4])


    def configure_consumption_coal_sliders(self):
        self.thermal_coal_consumption_slider_1.setValue(FUEL_COST_DEFAULT[0])
        self.thermal_coal_consumption_slider_2.setValue(FUEL_COST_DEFAULT[1])
        self.thermal_coal_consumption_slider_3.setValue(FUEL_COST_DEFAULT[2])
        self.thermal_coal_consumption_slider_4.setValue(FUEL_COST_DEFAULT[3])
        self.thermal_coal_consumption_slider_5.setValue(FUEL_COST_DEFAULT[4])
