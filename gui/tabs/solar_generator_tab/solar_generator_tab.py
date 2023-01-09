from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui.tabs.solar_generator_tab.solar_generator_tab_configure import SolarGeneratorTabConfigure
from load_optimization.generator_enum import GeneratorType
from load_optimization.generator.solar import SolarGenerator

class SolarGeneratorTab(SolarGeneratorTabConfigure):
    def __init__(self, tab: QWidget) -> None:
        super(SolarGeneratorTab, self).__init__(tab)
        generator = self.get_solar_generator_model()

    def get_solar_generator_model(self):
        # max_power = self.max_prod_solar_edit_line.value()
        # min_power = self.min_prod_solar_edit_line.value()
        #will be determine by iradiation
        max_power = 0
        min_power = 0
        panel_size = self.solar_panel_size_spin_box.value()
        efficiency = self.solar_panel_efficiency_spin_box.value()
        solar_generator_count = self.solar_panel_count_spin_box.value()

        solar_generator = SolarGenerator(
            max_power,
            min_power,
            GeneratorType.SOLAR,
            panel_size,
            efficiency,
            solar_generator_count
        )

        return solar_generator