from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtChart import QChart, QChartView, QPieSeries

import pyqtgraph as pg

class OptimizeTab():
    def __init__(self, tab:QWidget) -> None:
        self.cost_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'cost_weighted_factor_spin_box')
        self.co2_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'co2_weighted_factor_spin_box')

        self.generator_load_table:QTableWidget = tab.findChild(QTableWidget, 'generator_load_table')
        self.generator_cost_table:QTableWidget = tab.findChild(QTableWidget, 'generator_cost_table')
        self.generator_co2_emission_table:QTableWidget = tab.findChild(QTableWidget, 'generator_co2_emission_table')

        self.pie_chart_distribution:QChartView = tab.findChild(QChartView, 'pie_chart_distribution')

        self.hour_generator_load_slider:QSlider = tab.findChild(QSlider, 'hour_generator_load_slider')

        self.hour_generator_load_slider.valueChanged.connect(self.update_pie_distribution_chart)
        self.cost_weighted_factor_spin_box.valueChanged.connect(self.update_cost_spin_box)
        self.co2_weighted_factor_spin_box.valueChanged.connect(self.update_co2_spin_box)


    def set_generator_values(self, generator_loads, generator_costs, generator_co2_emissions):
        self.generator_loads = generator_loads
        self.generator_costs = generator_costs
        self.generator_co2_emissions = generator_co2_emissions

        self.hour_generator_load_slider.setValue(0)
        self.update_pie_distribution_chart(0)


    def update_cost_spin_box(self):
        cost_weight = self.get_cost_weight_factor()

        self.co2_weighted_factor_spin_box.setValue(1 - cost_weight)


    def update_co2_spin_box(self):
        co2_weight = self.get_co2_weight_factor()

        self.cost_weighted_factor_spin_box.setValue(1 - co2_weight)


    def get_cost_weight_factor(self):
        return self.cost_weighted_factor_spin_box.value()

    def get_co2_weight_factor(self):
        return self.co2_weighted_factor_spin_box.value()


    def update_generator_load_table(self):
        self.generator_load_table.setRowCount(len(self.generator_loads))
        self.generator_load_table.setColumnCount(len(self.generator_loads[0]))

        self.generator_load_table.setHorizontalHeaderLabels(list(self.generator_loads[0].keys()))

        keys = list(self.generator_loads[0].keys())

        for i in range(len(self.generator_loads)):
            for j in range(len(self.generator_loads[0])):
                key = keys[j]
                self.generator_load_table.setItem(i, j, QTableWidgetItem(str(self.generator_loads[i][key]) + ' MW'))

        self.generator_load_table.resizeColumnsToContents()


    def update_generator_cost_table(self):
        self.generator_cost_table.setRowCount(len(self.generator_costs))
        self.generator_cost_table.setColumnCount(len(self.generator_costs[0]))

        self.generator_cost_table.setHorizontalHeaderLabels(list(self.generator_costs[0].keys()))

        keys = list(self.generator_costs[0].keys())

        for i in range(len(self.generator_costs)):
            for j in range(len(self.generator_costs[0])):
                key = keys[j]
                self.generator_cost_table.setItem(i, j, QTableWidgetItem(str(self.generator_costs[i][key]) + ' $'))

        self.generator_cost_table.resizeColumnsToContents()


    def update_generator_co2_emission_table(self):
        self.generator_co2_emission_table.setRowCount(len(self.generator_co2_emissions))
        self.generator_co2_emission_table.setColumnCount(len(self.generator_co2_emissions[0]))

        self.generator_co2_emission_table.setHorizontalHeaderLabels(list(self.generator_co2_emissions[0].keys()))

        keys = list(self.generator_co2_emissions[0].keys())

        for i in range(len(self.generator_co2_emissions)):
            for j in range(len(self.generator_co2_emissions[0])):
                key = keys[j]
                self.generator_co2_emission_table.setItem(i, j, QTableWidgetItem(str(self.generator_co2_emissions[i][key]) + ' ton'))

        self.generator_co2_emission_table.resizeColumnsToContents()


    def update_pie_distribution_chart(self, value):
        series = QPieSeries()

        coal_power = 0
        gas_power = 0
        hydro_power = 0
        wind_power = 0
        solar_power = 0

        generator_hour_load = self.generator_loads[value]

        for key, load in generator_hour_load.items():
            if 'coal' in key:
                coal_power += load
            elif 'gas' in key:
                gas_power += load
            elif 'hydro' in key:
                hydro_power += load
            elif 'wind' in key:
                wind_power += load
            elif 'solar' in key:
                solar_power += load

        series.append('Coal', coal_power)
        series.append('Gas', gas_power)
        series.append('Hydro', hydro_power)
        series.append('Wind', wind_power)
        series.append('Solar', solar_power)

        series.clicked.connect(self.slice_clicked)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle('Power production distributed between generators')

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.legend()

        self.pie_chart_distribution.setChart(chart)
        self.pie_chart_distribution.setRenderHint(QPainter.Antialiasing)

        self.pie_chart_distribution.show()


    def slice_clicked(self, slice):
        slice.setExploded()
        slice.setLabelVisible()
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)
