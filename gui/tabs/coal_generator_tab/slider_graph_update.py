from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyqtgraph as pg

RANGE = [20, 40, 60, 80, 100]
DEFAULT_COLOR = 'r'


class CoalTabSliderGraphUpdate():
    def __init__(self, tab:QWidget) -> None:

        self.thermal_coal_slider_1 = tab.findChild(QSlider, 'thermal_coal_slider_1')
        self.thermal_coal_slider_2 = tab.findChild(QSlider, 'thermal_coal_slider_2')
        self.thermal_coal_slider_3 = tab.findChild(QSlider, 'thermal_coal_slider_3')
        self.thermal_coal_slider_4 = tab.findChild(QSlider, 'thermal_coal_slider_4')
        self.thermal_coal_slider_5 = tab.findChild(QSlider, 'thermal_coal_slider_5')

        self.thermal_coal_co2_cost_slider_1 = tab.findChild(QSlider, 'thermal_coal_co2_cost_slider_1')
        self.thermal_coal_co2_cost_slider_2 = tab.findChild(QSlider, 'thermal_coal_co2_cost_slider_2')
        self.thermal_coal_co2_cost_slider_3 = tab.findChild(QSlider, 'thermal_coal_co2_cost_slider_3')
        self.thermal_coal_co2_cost_slider_4 = tab.findChild(QSlider, 'thermal_coal_co2_cost_slider_4')
        self.thermal_coal_co2_cost_slider_5 = tab.findChild(QSlider, 'thermal_coal_co2_cost_slider_5')

        self.thermal_coal_consumption_slider_1 = tab.findChild(QSlider, 'thermal_coal_consumption_slider_1')
        self.thermal_coal_consumption_slider_2 = tab.findChild(QSlider, 'thermal_coal_consumption_slider_2')
        self.thermal_coal_consumption_slider_3 = tab.findChild(QSlider, 'thermal_coal_consumption_slider_3')
        self.thermal_coal_consumption_slider_4 = tab.findChild(QSlider, 'thermal_coal_consumption_slider_4')
        self.thermal_coal_consumption_slider_5 = tab.findChild(QSlider, 'thermal_coal_consumption_slider_5')

        self.thermal_coal_graphicview = tab.findChild(pg.PlotWidget, 'thermal_coal_graphicview')
        self.thermal_coal_co2_cost_graphicview = tab.findChild(pg.PlotWidget, 'thermal_coal_co2_cost_graphicview')
        self.thermal_coal_consumption_graphicview = tab.findChild(pg.PlotWidget, 'thermal_coal_consumption_graphicview')

        self.max_thermal_coal_power_spin_box = tab.findChild(QDoubleSpinBox, 'max_thermal_coal_power_spin_box')
        self.min_thermal_coal_power_spin_box = tab.findChild(QDoubleSpinBox, 'min_thermal_coal_power_spin_box')
        self.coal_cost_spin_box = tab.findChild(QDoubleSpinBox, 'coal_cost_spin_box')
        self.thermal_coal_count_spin_box = tab.findChild(QSpinBox, 'thermal_coal_count_spin_box')

        self.connect_value_change()


    def connect_value_change(self):
        self.thermal_coal_slider_1.valueChanged.connect(self.update_coal_co2_emission)
        self.thermal_coal_slider_2.valueChanged.connect(self.update_coal_co2_emission)
        self.thermal_coal_slider_3.valueChanged.connect(self.update_coal_co2_emission)
        self.thermal_coal_slider_4.valueChanged.connect(self.update_coal_co2_emission)
        self.thermal_coal_slider_5.valueChanged.connect(self.update_coal_co2_emission)

        self.thermal_coal_co2_cost_slider_1.valueChanged.connect(self.update_coal_co2_cost)
        self.thermal_coal_co2_cost_slider_2.valueChanged.connect(self.update_coal_co2_cost)
        self.thermal_coal_co2_cost_slider_3.valueChanged.connect(self.update_coal_co2_cost)
        self.thermal_coal_co2_cost_slider_4.valueChanged.connect(self.update_coal_co2_cost)
        self.thermal_coal_co2_cost_slider_5.valueChanged.connect(self.update_coal_co2_cost)

        self.thermal_coal_consumption_slider_1.valueChanged.connect(self.update_coal_consumption)
        self.thermal_coal_consumption_slider_2.valueChanged.connect(self.update_coal_consumption)
        self.thermal_coal_consumption_slider_3.valueChanged.connect(self.update_coal_consumption)
        self.thermal_coal_consumption_slider_4.valueChanged.connect(self.update_coal_consumption)
        self.thermal_coal_consumption_slider_5.valueChanged.connect(self.update_coal_consumption)


    def get_coal_co2_emission_slider_value(self):
        value_1 = self.thermal_coal_slider_1.value()
        value_2 = self.thermal_coal_slider_2.value()
        value_3 = self.thermal_coal_slider_3.value()
        value_4 = self.thermal_coal_slider_4.value()
        value_5 = self.thermal_coal_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_coal_co2_cost_slider_value(self):
        value_1 = self.thermal_coal_co2_cost_slider_1.value()
        value_2 = self.thermal_coal_co2_cost_slider_2.value()
        value_3 = self.thermal_coal_co2_cost_slider_3.value()
        value_4 = self.thermal_coal_co2_cost_slider_4.value()
        value_5 = self.thermal_coal_co2_cost_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_coal_consumption_slider_value(self):
        value_1 = self.thermal_coal_consumption_slider_1.value()
        value_2 = self.thermal_coal_consumption_slider_2.value()
        value_3 = self.thermal_coal_consumption_slider_3.value()
        value_4 = self.thermal_coal_consumption_slider_4.value()
        value_5 = self.thermal_coal_consumption_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def update_coal_co2_emission(self):
        value_list = self.get_coal_co2_emission_slider_value()

        self.thermal_coal_graphicview.clear()

        self.thermal_coal_graphicview.setBackground('w')

        self.thermal_coal_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_coal_graphicview.setLabel("left", "Emission", **styles)
        self.thermal_coal_graphicview.setLabel("bottom", "Power", **styles)

        self.thermal_coal_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_coal_graphicview.plot(RANGE, value_list, name='co2 coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_coal_co2_cost(self):
        value_list = self.get_coal_co2_cost_slider_value()

        self.thermal_coal_co2_cost_graphicview.clear()

        self.thermal_coal_co2_cost_graphicview.setBackground('w')

        self.thermal_coal_co2_cost_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_coal_co2_cost_graphicview.setLabel("left", "Cost", **styles)
        self.thermal_coal_co2_cost_graphicview.setLabel("bottom", "Power", **styles)

        self.thermal_coal_co2_cost_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_coal_co2_cost_graphicview.plot(RANGE, value_list, name='co2 cost', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_coal_consumption(self):
        value_list = self.get_coal_consumption_slider_value()

        self.thermal_coal_consumption_graphicview.clear()

        self.thermal_coal_consumption_graphicview.setBackground('w')

        self.thermal_coal_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_coal_consumption_graphicview.setLabel("left", "Cost", **styles)
        self.thermal_coal_consumption_graphicview.setLabel("bottom", "Power", **styles)

        self.thermal_coal_consumption_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_coal_consumption_graphicview.plot(RANGE, value_list, name='consumption coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))
