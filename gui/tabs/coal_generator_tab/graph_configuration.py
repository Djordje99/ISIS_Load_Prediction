from PyQt5.QtWidgets import QWidget

from gui.tabs.coal_generator_tab.slider_configuration import CoalTabSliderConfiguration, EMISSION_DEFAULT, CO2_COST_DEFAULT, FUEL_COST_DEFAULT



class CoalTabGraphConfiguration(CoalTabSliderConfiguration):
    def __init__(self, tab:QWidget) -> None:
        super().__init__(tab)
    #     self.set_graphics()


    # def set_graphics(self):
    #     self.configure_co2_coal_graph()
    #     self.configure_co2_cost_graph()
    #     self.configure_consumption_coal_graph()


    # def configure_co2_coal_graph(self):
    #     self.thermal_coal_graphicview.clear()

    #     self.thermal_coal_graphicview.setBackground('w')

    #     self.thermal_coal_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

    #     styles = {"color": "#f00", "font-size": "10px"}
    #     self.thermal_coal_graphicview.setLabel("left", "Emission [t]", **styles)
    #     self.thermal_coal_graphicview.setLabel("bottom", "Power [MW]", **styles)

    #     self.thermal_coal_graphicview.addLegend()

    #     pen = pg.mkPen(color=DEFAULT_COLOR)

    #     self.thermal_coal_graphicview.plot(RANGE, EMISSION_DEFAULT, name='co2 emission coal', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    # def configure_co2_cost_graph(self):
    #     self.thermal_coal_co2_cost_graphicview.clear()

    #     self.thermal_coal_co2_cost_graphicview.setBackground('w')

    #     self.thermal_coal_co2_cost_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

    #     styles = {"color": "#f00", "font-size": "10px"}
    #     self.thermal_coal_co2_cost_graphicview.setLabel("left", "Cost [$]", **styles)
    #     self.thermal_coal_co2_cost_graphicview.setLabel("bottom", "Tons [t]", **styles)

    #     self.thermal_coal_co2_cost_graphicview.addLegend()

    #     pen = pg.mkPen(color=DEFAULT_COLOR)

    #     self.thermal_coal_co2_cost_graphicview.plot(RANGE, CO2_COST_DEFAULT, name='co2 cost', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    # def configure_consumption_coal_graph(self):
    #     self.thermal_coal_consumption_graphicview.clear()

    #     self.thermal_coal_consumption_graphicview.setBackground('w')

    #     self.thermal_coal_consumption_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

    #     styles = {"color": "#f00", "font-size": "10px"}
    #     self.thermal_coal_consumption_graphicview.setLabel("left", "Cost [$]", **styles)
    #     self.thermal_coal_consumption_graphicview.setLabel("bottom", "Power [MW]", **styles)

    #     self.thermal_coal_consumption_graphicview.addLegend()

    #     pen = pg.mkPen(color=DEFAULT_COLOR)

    #     self.thermal_coal_consumption_graphicview.plot(RANGE, FUEL_COST_DEFAULT, name='coal consumption', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))
