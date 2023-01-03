from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import numpy as np

from gui.configuration.graph_configuration import GraphConfiguration
from gui.configuration.slider_configuration import SliderConfiguration
from gui.configuration.slider_graph_update import SliderGraphUpdate

class ConfigurationTab(GraphConfiguration):
    def __init__(self, window) -> None:
        super(ConfigurationTab, self).__init__(window)
        self.slicer = SliderConfiguration(self.window)
        self.graph_update = SliderGraphUpdate(self.window)

