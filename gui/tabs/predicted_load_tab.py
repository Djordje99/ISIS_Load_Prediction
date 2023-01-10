from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import numpy as np

from database.controller import DatabaseController
from services.scorer.scrorer import Scorer


class PredictedLoadTab():
    def __init__(self, tab:QWidget) -> None:
        self.database_controller = DatabaseController()
        self.scorer = Scorer()

        self.graphicsView = tab.findChild(pg.PlotWidget, 'graphicsView')
        self.mape_edit_line = tab.findChild(QLineEdit, 'mape_edit_line')
        self.mse_edit_line = tab.findChild(QLineEdit, 'mse_edit_line')

        self.configure_graph()
        self.plot_graph()


    def refresh_graph(self):
        self.graphicsView.clear()
        self.configure_graph()
        self.plot_graph()


    def calculate_error(self, load, predicted_load):
        mape_error = self.scorer.get_mean_absolute_percentage_error(load, predicted_load)
        mse_error = self.scorer.get_mean_square_error(load, predicted_load)

        self.mape_edit_line.setText(f'{round(mape_error, 4)}% MAPE')
        self.mse_edit_line.setText(f'{round(mse_error, 4)} MSE')


    def plot_graph(self):
        hours = range(0, 24)
        predicted_load, date_form, date_to = self.get_predicted_load()
        load_data = self.get_real_load(date_form, date_to)

        if not load_data.empty:
            self.plot(hours, load_data, 'Load', 'blue')
            self.calculate_error(load_data, predicted_load)

        self.plot(hours, predicted_load, 'Predicted Load', 'r')

    def get_predicted_load(self):
        data_frame = self.database_controller.load_predicted_load()
        data_frame = data_frame.head(24)

        return data_frame["predicted_load"], data_frame['date'].min(), data_frame['date'].max()


    def get_real_load(self, date_from, date_to):
        data_frame = self.database_controller.load_training_data(date_from, date_to)
        data_frame = data_frame.head(24)

        return data_frame['load']


    def configure_graph(self):
        self.graphicsView.setBackground('w')

        self.graphicsView.setTitle(color="b", size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.graphicsView.setLabel("left", "Load", **styles)
        self.graphicsView.setLabel("bottom", "Hour", **styles)

        self.graphicsView.addLegend()

        self.graphicsView.showGrid(x=True, y=True)
        #Set Range
        self.graphicsView.setXRange(0, 10, padding=0)
        self.graphicsView.setYRange(20, 55, padding=0)

    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphicsView.plot(x, y, name=plotname, pen=pen, symbolSize=6, symbolBrush=(color))