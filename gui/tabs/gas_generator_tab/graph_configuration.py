import pyqtgraph as pg

from gui.tabs.gas_generator_tab.slider_configuration import GasTabSliderConfiguration

FUEL_COST_DEFAULT = [20, 40, 65, 80, 100]
EMISSION_DEFAULT = [40, 20, 45, 75, 100]
RANGE = [20, 40, 60, 80, 100]
DEFAULT_COLOR = 'r'


class GasTabGraphConfiguration(GasTabSliderConfiguration):
    def __init__(self, window) -> None:
        super(GasTabGraphConfiguration, self).__init__(window)
        self.window = window
        self.set_graphics()


    def set_graphics(self):
        self.configure_co2_gas_graph()
        self.configure_consumption_gas_graph()


    def configure_co2_gas_graph(self):
        self.window.thermal_gas_graphicview.setBackground('w')

        self.window.thermal_gas_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_gas_graphicview.setLabel("left", "Emission", **styles)
        self.window.thermal_gas_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_gas_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_gas_graphicview.plot(RANGE, EMISSION_DEFAULT, name='co2 gas', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def configure_consumption_gas_graph(self):
        self.window.thermal_gas_consumption_graphicview.setBackground('w')

        self.window.thermal_gas_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.thermal_gas_consumption_graphicview.setLabel("left", "Cost", **styles)
        self.window.thermal_gas_consumption_graphicview.setLabel("bottom", "Power", **styles)

        self.window.thermal_gas_consumption_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.thermal_gas_consumption_graphicview.plot(RANGE, FUEL_COST_DEFAULT, name='consumption coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))
