from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui.tabs.solar_generator_tab.configuration import Configuration
from load_optimization.enum.generator_enum import GeneratorType
from load_optimization.generator_model.solar import SolarGenerator

class SolarGeneratorTab(Configuration):
    def __init__(self, tab: QWidget) -> None:
        super(SolarGeneratorTab, self).__init__(tab)
