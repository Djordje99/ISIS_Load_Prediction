from gui.tabs.gas_generator_tab.slider_configuration import GasTabSliderConfiguration


class GasTabGraphConfiguration(GasTabSliderConfiguration):
    def __init__(self, tab) -> None:
        super(GasTabGraphConfiguration, self).__init__(tab)
    #     self.set_graphics()


    # def set_graphics(self):
    #     self.configure_co2_gas_graph()
    #     self.configure_consumption_gas_graph()


    # def configure_co2_gas_graph(self):
    #     self.thermal_gas_graphicview.setBackground('w')

    #     self.thermal_gas_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

    #     styles = {"color": "#f00", "font-size": "10px"}
    #     self.thermal_gas_graphicview.setLabel("left", "Emission", **styles)
    #     self.thermal_gas_graphicview.setLabel("bottom", "Power", **styles)

    #     self.thermal_gas_graphicview.addLegend()

    #     pen = pg.mkPen(color=DEFAULT_COLOR)

    #     self.thermal_gas_graphicview.plot(RANGE, EMISSION_DEFAULT, name='co2 gas', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    # def configure_consumption_gas_graph(self):
    #     self.thermal_gas_consumption_graphicview.setBackground('w')

    #     self.thermal_gas_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

    #     styles = {"color": "#f00", "font-size": "10px"}
    #     self.thermal_gas_consumption_graphicview.setLabel("left", "Cost", **styles)
    #     self.thermal_gas_consumption_graphicview.setLabel("bottom", "Power", **styles)

    #     self.thermal_gas_consumption_graphicview.addLegend()

    #     pen = pg.mkPen(color=DEFAULT_COLOR)

    #     self.thermal_gas_consumption_graphicview.plot(RANGE, FUEL_COST_DEFAULT, name='consumption coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))
