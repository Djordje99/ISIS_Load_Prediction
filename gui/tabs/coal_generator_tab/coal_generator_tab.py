from gui.tabs.coal_generator_tab.graph_configuration import CoalTabGraphConfiguration


class CoalGeneratorTab(CoalTabGraphConfiguration):
    def __init__(self, window) -> None:
        super(CoalGeneratorTab, self).__init__(window)


    def get_coal_generator_data(self):
        coal_consumption = self.get_coal_consumption_slider_value()
