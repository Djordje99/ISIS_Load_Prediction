import pyqtgraph as pg
import math

HOURS = [i for i in range(0, 24)]
IRRADIANCE = [0,0,0,0,0,0,15, 68, 181, 412, 628, 811, 900, 954, 898, 787, 339, 211, 75, 57, 42, 0, 0, 0,]
DEFAULT_COLOR = 'r'


class SolarGeneratorTab():
    def __init__(self, window) -> None:
        self.window = window
        self.connect_spin_box()
        self.update_graph()


    def connect_spin_box(self):
        self.window.solar_panel_size_spin_box.valueChanged.connect(self.update_graph)
        self.window.solar_panel_efficiency_label_spin_box.valueChanged.connect(self.update_graph)


    def get_spin_box_value(self):
        value_1 = self.window.solar_panel_size_spin_box.value()
        value_2 = self.window.solar_panel_efficiency_label_spin_box.value()

        return value_1, value_2


    def solar_panel_power_output(self, size, efficiency, irradiance):
        power = size * efficiency * irradiance
        return power / 1000000


    def update_graph(self):
        panel_size, efficiency = self.get_spin_box_value()
        power_output = []

        for hour in HOURS:
            power = self.solar_panel_power_output(panel_size, efficiency, IRRADIANCE[hour])
            power_output.append(power)

        self.plot_graph(power_output)
        self.set_max_min_power(power_output)


    def plot_graph(self, power_output):
        self.window.solar_panel_power_output_graphicview.clear()

        self.window.solar_panel_power_output_graphicview.setBackground('w')

        self.window.solar_panel_power_output_graphicview.setTitle(color=DEFAULT_COLOR, size="30pt")

        styles = {"color": "#f00", "font-size": "10px"}
        self.window.solar_panel_power_output_graphicview.setLabel("left", "Power (MW)", **styles)
        self.window.solar_panel_power_output_graphicview.setLabel("bottom", "Hour (h)", **styles)

        self.window.solar_panel_power_output_graphicview.addLegend()

        pen = pg.mkPen(color=DEFAULT_COLOR)

        self.window.solar_panel_power_output_graphicview.plot(HOURS, power_output, name='power', pen=pen, symbolSize=3, symbolBrush=(DEFAULT_COLOR))


    def set_max_min_power(self, power_output):
        self.window.max_prod_solar_edit_line.setText(f'{round(max(power_output), 4)} MW')
        self.window.min_prod_solar_edit_line.setText(f'{round(min(power_output), 4)} MW')