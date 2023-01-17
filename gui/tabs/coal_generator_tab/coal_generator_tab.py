from PyQt5.QtWidgets import QWidget

from gui.tabs.coal_generator_tab.slider_configuration import CoalTabSliderConfiguration


class CoalGeneratorTab(CoalTabSliderConfiguration):
    def __init__(self, tab:QWidget) -> None:
        super(CoalGeneratorTab, self).__init__(tab)
