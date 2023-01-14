from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui.tabs.wind_generator_tab.configuration import Configuration
from load_optimization.enum.generator_enum import GeneratorType
from load_optimization.generator_model.wind import WindGenerator

class WindGeneratorTab(Configuration):
    def __init__(self, tab: QWidget) -> None:
        super().__init__(tab)
