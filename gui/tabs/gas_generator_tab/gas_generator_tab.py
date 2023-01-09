from gui.tabs.gas_generator_tab.graph_configuration import GasTabGraphConfiguration
from gui.tabs.gas_generator_tab.slider_configuration import GasTabSliderConfiguration
from gui.tabs.gas_generator_tab.slider_graph_update import GasTabSliderGraphUpdate


class GasGeneratorTab(GasTabGraphConfiguration):
    def __init__(self, window) -> None:
        super(GasGeneratorTab, self).__init__(window)
        self.slicer = GasTabSliderConfiguration(self.window)
        self.graph_update = GasTabSliderGraphUpdate(self.window)