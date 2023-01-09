from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
from math import pow

WIND_SPEED = [i for i in range(0, 41)]
AIR_DENSITY = 1.225
DEFAULT_COLOR = 'r'


class WindGeneratorTab():
    def __init__(self, tab:QWidget) -> None:
        self.cross_sectional_aria_wind_spin_box = tab.findChild(QDoubleSpinBox, 'cross_sectional_aria_wind_spin_box')
        self.cut_in_speed_spin_box = tab.findChild(QDoubleSpinBox, 'cut_in_speed_spin_box')
        self.cut_out_speed_spin_box = tab.findChild(QDoubleSpinBox, 'cut_out_speed_spin_box')
        self.wind_generator_power_graphicview = tab.findChild(pg.PlotWidget, 'wind_generator_power_graphicview')
        self.max_prod_wind_edit_line = tab.findChild(QLineEdit, 'max_prod_wind_edit_line')
        self.min_prod_wind_edit_line = tab.findChild(QLineEdit, 'min_prod_wind_edit_line')

        self.connect_spin_box()
        self.update_graph()


    def connect_spin_box(self):
        self.cross_sectional_aria_wind_spin_box.valueChanged.connect(self.update_graph)
        self.cut_in_speed_spin_box.valueChanged.connect(self.update_graph)
        self.cut_out_speed_spin_box.valueChanged.connect(self.update_graph)


    def get_spin_box_value(self):
        value_1 = self.cross_sectional_aria_wind_spin_box.value()
        value_2 = self.cut_in_speed_spin_box.value()
        value_3 = self.cut_out_speed_spin_box.value()

        return value_1, value_2, value_3


    def wind_generator_power_output(self, rho, cross_section, wind_speed):
        power = (1/2) * rho * cross_section * pow(wind_speed, 3)
        return power / 1000000


    def update_graph(self):
        cross_section, cut_in, cut_out = self.get_spin_box_value()
        power_output = []

        for wind_speed in WIND_SPEED:
            if wind_speed <= cut_in or wind_speed >= cut_out:
                power_output.append(0)
            else:
                power_value = self.wind_generator_power_output(AIR_DENSITY, cross_section, wind_speed)
                power_output.append(power_value)

        self.plot_graph(power_output)
        self.set_max_min_power(power_output)


    def plot_graph(self, power_output):
        self.wind_generator_power_graphicview.clear()

        self.wind_generator_power_graphicview.setBackground('w')

        self.wind_generator_power_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.wind_generator_power_graphicview.setLabel("left", "Power (MW)", **styles)
        self.wind_generator_power_graphicview.setLabel("bottom", "Wind Speed (m/s)", **styles)

        self.wind_generator_power_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.wind_generator_power_graphicview.plot(WIND_SPEED, power_output, name='power', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def set_max_min_power(self, power_output):
        self.max_prod_wind_edit_line.setText(f'{round(max(power_output), 4)} MW')
        self.min_prod_wind_edit_line.setText(f'{round(min(power_output), 4)} MW')
