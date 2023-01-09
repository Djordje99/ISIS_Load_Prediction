from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import numpy as np

from gui.configuration.graph_configuration import GraphConfiguration
from gui.configuration.slider_configuration import SliderConfiguration
from gui.configuration.slider_graph_update import SliderGraphUpdate

from load_optimization.generator_model_creator import GeneratorModelCreator

class ConfigurationTab(GraphConfiguration):
    def __init__(self, window) -> None:
        super(ConfigurationTab, self).__init__(window)
        self.slicer = SliderConfiguration(self.window)
        self.graph_update = SliderGraphUpdate(self.window)
        self.generator_creator = GeneratorModelCreator()

    #     self.connect_buttons()


    # def connect_buttons(self):
    #     self.window.optimize_btn.clicked.connect(self.create_models)


    # def create_models(self):
    #     self.get_thermal_coal_data()

    #     self.generator_creator.create_thermal_coal_generator()

