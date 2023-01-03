from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import numpy as np

from database.controller import DatabaseController
from services.scorer.scrorer import Scorer


class PredictionTab():
    def __init__(self, window) -> None:
        self.database_controller = DatabaseController()
        self.scorer = Scorer()
        self.window = window
        self.configure_graph()
        self.plot_graph()


    def refresh_graph(self):
        self.window.graphicsView.clear()
        self.configure_graph()
        self.plot_graph()


    def calculate_error(self, load, predicted_load):
        mape_error = self.scorer.get_mean_absolute_percentage_error(load, predicted_load)
        mse_error = self.scorer.get_mean_square_error(load, predicted_load)

        self.window.mape_edit_line.setText(f'{round(mape_error, 4)}% MAPE')
        self.window.mse_edit_line.setText(f'{round(mse_error, 4)} MSE')


    def plot_graph(self):
        predicted_load, date_form, date_to = self.get_predicted_load()
        load_data = self.get_real_load(date_form, date_to)
        hours = range(0, 24)

        self.plot(hours, load_data, 'Load', 'blue')
        self.plot(hours, predicted_load, 'PredictedLoad', 'r')

        self.calculate_error(load_data, predicted_load)


    def get_predicted_load(self):
        data_frame = self.database_controller.load_predicted_load()
        data_frame = data_frame.head(24)

        return data_frame["predicted_load"], data_frame['date'].min(), data_frame['date'].max()


    def get_real_load(self, date_from, date_to):
        data_frame = self.database_controller.get_data_frame_from_date(date_from, date_to)
        data_frame = data_frame.head(24)

        return data_frame['load']


    def configure_graph(self):
        self.window.graphicsView.setBackground('w')

        self.window.graphicsView.setTitle("Your Title Here", color="b", size="30pt")

        styles = {"color": "#f00", "font-size": "20px"}
        self.window.graphicsView.setLabel("left", "Load", **styles)
        self.window.graphicsView.setLabel("bottom", "Hour", **styles)

        self.window.graphicsView.addLegend()


    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.window.graphicsView.plot(x, y, name=plotname, pen=pen, symbolSize=30, symbolBrush=(color))