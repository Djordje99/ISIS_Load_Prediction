from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import numpy as np

from database.controller import DatabaseController

class PredictionTab():
    def __init__(self, window) -> None:
        self.database_controller = DatabaseController()
        self.window = window
        self.configure_graph()
        self.plot_predicted_load()


    def plot_predicted_load(self):
        data_frame = self.database_controller.load_predicted_load()
        data_frame = data_frame.head(24)
        hours = range(0, 24)
        self.plot(hours, data_frame['predicted_load'], 'PredictedLoad', 'r')

    def configure_graph(self):
        self.window.graphicsView.setBackground('w')
        # Add Title
        self.window.graphicsView.setTitle("Your Title Here", color="b", size="30pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.window.graphicsView.setLabel("left", "Load", **styles)
        self.window.graphicsView.setLabel("bottom", "Hour", **styles)
        #Add legend
        self.window.graphicsView.addLegend()
        #Add grid
        self.window.graphicsView.showGrid(x=True, y=True)
        #Set Range
        self.window.graphicsView.setXRange(0, 10, padding=0)
        self.window.graphicsView.setYRange(20, 55, padding=0)


    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.window.graphicsView.plot(x, y, name=plotname, pen=pen, symbol='o', symbolSize=30, symbolBrush=(color))