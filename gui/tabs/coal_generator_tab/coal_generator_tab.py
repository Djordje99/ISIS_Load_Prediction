from gui.tabs.coal_generator_tab.graph_configuration import CoalTabGraphConfiguration
from gui.tabs.coal_generator_tab.slider_configuration import CoalTabSliderConfiguration
from gui.tabs.coal_generator_tab.slider_graph_update import CoalTabSliderGraphUpdate


class CoalGeneratorTab(CoalTabGraphConfiguration):
    def __init__(self, window) -> None:
        super(CoalGeneratorTab, self).__init__(window)
        self.slicer = CoalTabSliderConfiguration(self.window)
        self.graph_update = CoalTabSliderGraphUpdate(self.window)