import pyqtgraph as pg

RANGE = [20, 40, 60, 80, 100]
DEFAULT_COLOR = 'r'


class SliderGraphUpdate():
    def __init__(self, window) -> None:
        self.window = window
        self.connect_value_change()


    def connect_value_change(self):
        self.window.thermal_coal_slider_1.valueChanged.connect(self.update_coal_co2_emission)
        self.window.thermal_coal_slider_2.valueChanged.connect(self.update_coal_co2_emission)
        self.window.thermal_coal_slider_3.valueChanged.connect(self.update_coal_co2_emission)
        self.window.thermal_coal_slider_4.valueChanged.connect(self.update_coal_co2_emission)
        self.window.thermal_coal_slider_5.valueChanged.connect(self.update_coal_co2_emission)

        self.window.thermal_gas_slider_1.valueChanged.connect(self.update_gas_co2_emission)
        self.window.thermal_gas_slider_2.valueChanged.connect(self.update_gas_co2_emission)
        self.window.thermal_gas_slider_3.valueChanged.connect(self.update_gas_co2_emission)
        self.window.thermal_gas_slider_4.valueChanged.connect(self.update_gas_co2_emission)
        self.window.thermal_gas_slider_5.valueChanged.connect(self.update_gas_co2_emission)

        self.window.thermal_coal_consumption_slider_1.valueChanged.connect(self.update_coal_consumption)
        self.window.thermal_coal_consumption_slider_2.valueChanged.connect(self.update_coal_consumption)
        self.window.thermal_coal_consumption_slider_3.valueChanged.connect(self.update_coal_consumption)
        self.window.thermal_coal_consumption_slider_4.valueChanged.connect(self.update_coal_consumption)
        self.window.thermal_coal_consumption_slider_5.valueChanged.connect(self.update_coal_consumption)

        self.window.thermal_gas_consumption_slider_1.valueChanged.connect(self.update_gas_consumption)
        self.window.thermal_gas_consumption_slider_2.valueChanged.connect(self.update_gas_consumption)
        self.window.thermal_gas_consumption_slider_3.valueChanged.connect(self.update_gas_consumption)
        self.window.thermal_gas_consumption_slider_4.valueChanged.connect(self.update_gas_consumption)
        self.window.thermal_gas_consumption_slider_5.valueChanged.connect(self.update_gas_consumption)


    def get_coal_co2_emission_slider_value(self):
        value_1 = self.window.thermal_coal_slider_1.value()
        value_2 = self.window.thermal_coal_slider_2.value()
        value_3 = self.window.thermal_coal_slider_3.value()
        value_4 = self.window.thermal_coal_slider_4.value()
        value_5 = self.window.thermal_coal_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_gas_co2_emission_slider_value(self):
        value_1 = self.window.thermal_gas_slider_1.value()
        value_2 = self.window.thermal_gas_slider_2.value()
        value_3 = self.window.thermal_gas_slider_3.value()
        value_4 = self.window.thermal_gas_slider_4.value()
        value_5 = self.window.thermal_gas_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_coal_consumption_slider_value(self):
        value_1 = self.window.thermal_coal_consumption_slider_1.value()
        value_2 = self.window.thermal_coal_consumption_slider_2.value()
        value_3 = self.window.thermal_coal_consumption_slider_3.value()
        value_4 = self.window.thermal_coal_consumption_slider_4.value()
        value_5 = self.window.thermal_coal_consumption_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def get_gas_consumption_slider_value(self):
        value_1 = self.window.thermal_gas_consumption_slider_1.value()
        value_2 = self.window.thermal_gas_consumption_slider_2.value()
        value_3 = self.window.thermal_gas_consumption_slider_3.value()
        value_4 = self.window.thermal_gas_consumption_slider_4.value()
        value_5 = self.window.thermal_gas_consumption_slider_5.value()

        return [value_1, value_2, value_3, value_4, value_5]


    def update_coal_co2_emission(self):
        value_list = self.get_coal_co2_emission_slider_value()

        self.window.thermal_coal_graphicview.clear()

        self.window.thermal_coal_graphicview.setBackground('w')

        self.window.thermal_coal_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_coal_graphicview.setLabel("left", "Emission", **styles)
        self.window.thermal_coal_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_coal_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_coal_graphicview.plot(RANGE, value_list, name='co2 coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_gas_co2_emission(self):
        value_list = self.get_gas_co2_emission_slider_value()

        self.window.thermal_gas_graphicview.clear()

        self.window.thermal_gas_graphicview.setBackground('w')

        self.window.thermal_gas_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_gas_graphicview.setLabel("left", "Emission", **styles)
        self.window.thermal_gas_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_gas_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_gas_graphicview.plot(RANGE, value_list, name='co2 gas', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_coal_consumption(self):
        value_list = self.get_coal_consumption_slider_value()

        self.window.thermal_coal_consumption_graphicview.clear()

        self.window.thermal_coal_consumption_graphicview.setBackground('w')

        self.window.thermal_coal_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_coal_consumption_graphicview.setLabel("left", "Cost", **styles)
        self.window.thermal_coal_consumption_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_coal_consumption_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_coal_consumption_graphicview.plot(RANGE, value_list, name='consumption coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def update_gas_consumption(self):
        value_list = self.get_gas_consumption_slider_value()

        self.window.thermal_gas_consumption_graphicview.clear()

        self.window.thermal_gas_consumption_graphicview.setBackground('w')

        self.window.thermal_gas_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_gas_consumption_graphicview.setLabel("left", "Cost", **styles)
        self.window.thermal_gas_consumption_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_gas_consumption_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_gas_consumption_graphicview.plot(RANGE, value_list, name='consumption gas', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))

