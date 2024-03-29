from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg

RANGE = [20, 40, 60, 80, 100]
DEFAULT_COLOR = 'r'


class GasTabSliderGraphUpdate():
    def __init__(self, tab:QWidget) -> None:

        self.thermal_gas_slider_1 = tab.findChild(QSlider, 'thermal_gas_slider_1')
        self.thermal_gas_slider_2 = tab.findChild(QSlider, 'thermal_gas_slider_2')
        self.thermal_gas_slider_3 = tab.findChild(QSlider, 'thermal_gas_slider_3')
        self.thermal_gas_slider_4 = tab.findChild(QSlider, 'thermal_gas_slider_4')
        self.thermal_gas_slider_5 = tab.findChild(QSlider, 'thermal_gas_slider_5')

        self.thermal_gas_co2_cost_slider_1 = tab.findChild(QSlider, 'thermal_gas_co2_cost_slider_1')
        self.thermal_gas_co2_cost_slider_2 = tab.findChild(QSlider, 'thermal_gas_co2_cost_slider_2')
        self.thermal_gas_co2_cost_slider_3 = tab.findChild(QSlider, 'thermal_gas_co2_cost_slider_3')
        self.thermal_gas_co2_cost_slider_4 = tab.findChild(QSlider, 'thermal_gas_co2_cost_slider_4')
        self.thermal_gas_co2_cost_slider_5 = tab.findChild(QSlider, 'thermal_gas_co2_cost_slider_5')

        self.thermal_gas_consumption_slider_1 = tab.findChild(QSlider, 'thermal_gas_consumption_slider_1')
        self.thermal_gas_consumption_slider_2 = tab.findChild(QSlider, 'thermal_gas_consumption_slider_2')
        self.thermal_gas_consumption_slider_3 = tab.findChild(QSlider, 'thermal_gas_consumption_slider_3')
        self.thermal_gas_consumption_slider_4 = tab.findChild(QSlider, 'thermal_gas_consumption_slider_4')
        self.thermal_gas_consumption_slider_5 = tab.findChild(QSlider, 'thermal_gas_consumption_slider_5')

        self.thermal_gas_graphicview = tab.findChild(pg.PlotWidget, 'thermal_gas_graphicview')
        self.thermal_gas_consumption_graphicview = tab.findChild(pg.PlotWidget, 'thermal_gas_consumption_graphicview')
        self.thermal_gas_co2_cost_graphicview = tab.findChild(pg.PlotWidget, 'thermal_gas_co2_cost_graphicview')


        self.max_thermal_gas_power_spin_box = tab.findChild(QDoubleSpinBox, 'max_thermal_gas_power_spin_box')
        self.min_thermal_gas_power_spin_box = tab.findChild(QDoubleSpinBox, 'min_thermal_gas_power_spin_box')
        self.gas_cost_spin_box = tab.findChild(QDoubleSpinBox, 'gas_cost_spin_box')
        self.thermal_gas_count_spin_box = tab.findChild(QSpinBox, 'thermal_gas_count_spin_box')

        self.connect_value_change()


    def connect_value_change(self):
        self.thermal_gas_slider_1.valueChanged.connect(self.update_gas_co2_emission)
        self.thermal_gas_slider_2.valueChanged.connect(self.update_gas_co2_emission)
        self.thermal_gas_slider_3.valueChanged.connect(self.update_gas_co2_emission)
        self.thermal_gas_slider_4.valueChanged.connect(self.update_gas_co2_emission)
        self.thermal_gas_slider_5.valueChanged.connect(self.update_gas_co2_emission)

        self.thermal_gas_co2_cost_slider_1.valueChanged.connect(self.update_gas_co2_cost)
        self.thermal_gas_co2_cost_slider_2.valueChanged.connect(self.update_gas_co2_cost)
        self.thermal_gas_co2_cost_slider_3.valueChanged.connect(self.update_gas_co2_cost)
        self.thermal_gas_co2_cost_slider_4.valueChanged.connect(self.update_gas_co2_cost)
        self.thermal_gas_co2_cost_slider_5.valueChanged.connect(self.update_gas_co2_cost)

        self.thermal_gas_consumption_slider_1.valueChanged.connect(self.update_gas_consumption)
        self.thermal_gas_consumption_slider_2.valueChanged.connect(self.update_gas_consumption)
        self.thermal_gas_consumption_slider_3.valueChanged.connect(self.update_gas_consumption)
        self.thermal_gas_consumption_slider_4.valueChanged.connect(self.update_gas_consumption)
        self.thermal_gas_consumption_slider_5.valueChanged.connect(self.update_gas_consumption)


    def get_gas_co2_emission_slider_value(self):
        value_1 = self.thermal_gas_slider_1.value()
        value_2 = self.thermal_gas_slider_2.value()
        value_3 = self.thermal_gas_slider_3.value()
        value_4 = self.thermal_gas_slider_4.value()
        value_5 = self.thermal_gas_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_gas_co2_cost_slider_value(self):
        value_1 = self.thermal_gas_co2_cost_slider_1.value()
        value_2 = self.thermal_gas_co2_cost_slider_2.value()
        value_3 = self.thermal_gas_co2_cost_slider_3.value()
        value_4 = self.thermal_gas_co2_cost_slider_4.value()
        value_5 = self.thermal_gas_co2_cost_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_gas_consumption_slider_value(self):
        value_1 = self.thermal_gas_consumption_slider_1.value()
        value_2 = self.thermal_gas_consumption_slider_2.value()
        value_3 = self.thermal_gas_consumption_slider_3.value()
        value_4 = self.thermal_gas_consumption_slider_4.value()
        value_5 = self.thermal_gas_consumption_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def update_gas_co2_emission(self):
        value_list = self.get_gas_co2_emission_slider_value()

        self.thermal_gas_graphicview.clear()

        self.thermal_gas_graphicview.setBackground('w')

        self.thermal_gas_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_gas_graphicview.setLabel("left", "Emission [ton]", **styles)
        self.thermal_gas_graphicview.setLabel("bottom", "Power [MW]", **styles)

        self.thermal_gas_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_gas_graphicview.plot(RANGE, value_list, name='gas co2 emission', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_gas_co2_cost(self):
        value_list = self.get_gas_co2_cost_slider_value()

        self.thermal_gas_co2_cost_graphicview.clear()

        self.thermal_gas_co2_cost_graphicview.setBackground('w')

        self.thermal_gas_co2_cost_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_gas_co2_cost_graphicview.setLabel("left", "Cost [$]", **styles)
        self.thermal_gas_co2_cost_graphicview.setLabel("bottom", "Amount [ton]", **styles)

        self.thermal_gas_co2_cost_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_gas_co2_cost_graphicview.plot(RANGE, value_list, name='co2 cost', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_gas_consumption(self):
        value_list = self.get_gas_consumption_slider_value()

        self.thermal_gas_consumption_graphicview.clear()

        self.thermal_gas_consumption_graphicview.setBackground('w')

        self.thermal_gas_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.thermal_gas_consumption_graphicview.setLabel("left", "Consumption [ton]", **styles)
        self.thermal_gas_consumption_graphicview.setLabel("bottom", "Power [MW]", **styles)

        self.thermal_gas_consumption_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.thermal_gas_consumption_graphicview.plot(RANGE, value_list, name='gas consumption', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))

