FUEL_COST_DEFAULT = [20, 40, 65, 80, 100]
EMISSION_DEFAULT = [40, 20, 45, 75, 100]

class SliderConfiguration():
    def __init__(self, window) -> None:
        self.window = window
        self.configure_sliders()


    def configure_sliders(self):
        self.configure_co2_coal_sliders()
        self.configure_co2_gas_sliders()
        self.configure_consumption_coal_sliders()
        self.configure_consumption_gas_sliders()


    def configure_co2_coal_sliders(self):
        self.window.thermal_coal_slider_1.setValue(EMISSION_DEFAULT[0])
        self.window.thermal_coal_slider_2.setValue(EMISSION_DEFAULT[1])
        self.window.thermal_coal_slider_3.setValue(EMISSION_DEFAULT[2])
        self.window.thermal_coal_slider_4.setValue(EMISSION_DEFAULT[3])
        self.window.thermal_coal_slider_5.setValue(EMISSION_DEFAULT[4])


    def configure_co2_gas_sliders(self):
        self.window.thermal_gas_slider_1.setValue(EMISSION_DEFAULT[0])
        self.window.thermal_gas_slider_2.setValue(EMISSION_DEFAULT[1])
        self.window.thermal_gas_slider_3.setValue(EMISSION_DEFAULT[2])
        self.window.thermal_gas_slider_4.setValue(EMISSION_DEFAULT[3])
        self.window.thermal_gas_slider_5.setValue(EMISSION_DEFAULT[4])


    def configure_consumption_coal_sliders(self):
        self.window.thermal_coal_consumption_slider_1.setValue(FUEL_COST_DEFAULT[0])
        self.window.thermal_coal_consumption_slider_2.setValue(FUEL_COST_DEFAULT[1])
        self.window.thermal_coal_consumption_slider_3.setValue(FUEL_COST_DEFAULT[2])
        self.window.thermal_coal_consumption_slider_4.setValue(FUEL_COST_DEFAULT[3])
        self.window.thermal_coal_consumption_slider_5.setValue(FUEL_COST_DEFAULT[4])


    def configure_consumption_gas_sliders(self):
        self.window.thermal_gas_consumption_slider_1.setValue(FUEL_COST_DEFAULT[0])
        self.window.thermal_gas_consumption_slider_2.setValue(FUEL_COST_DEFAULT[1])
        self.window.thermal_gas_consumption_slider_3.setValue(FUEL_COST_DEFAULT[2])
        self.window.thermal_gas_consumption_slider_4.setValue(FUEL_COST_DEFAULT[3])
        self.window.thermal_gas_consumption_slider_5.setValue(FUEL_COST_DEFAULT[4])