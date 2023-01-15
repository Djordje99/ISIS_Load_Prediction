from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class OptimizeTab():
    def __init__(self, tab:QWidget) -> None:
        self.cost_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'cost_weighted_factor_spin_box')
        self.co2_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'co2_weighted_factor_spin_box')
        self.generator_load_table:QTableWidget = tab.findChild(QTableWidget, 'generator_load_table')
        self.generator_cost_table:QTableWidget = tab.findChild(QTableWidget, 'generator_cost_table')
        self.generator_co2_emission_table:QTableWidget = tab.findChild(QTableWidget, 'generator_co2_emission_table')

        self.cost_weighted_factor_spin_box.valueChanged.connect(self.update_cost_spin_box)
        self.co2_weighted_factor_spin_box.valueChanged.connect(self.update_co2_spin_box)


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


    def update_generator_load_table(self, generator_loads):
        self.generator_load_table.setRowCount(len(generator_loads))
        self.generator_load_table.setColumnCount(len(generator_loads[0]))

        self.generator_load_table.setHorizontalHeaderLabels(list(generator_loads[0].keys()))

        keys = list(generator_loads[0].keys())

        for i in range(len(generator_loads)):
            for j in range(len(generator_loads[0])):
                key = keys[j]
                self.generator_load_table.setItem(i, j, QTableWidgetItem(str(generator_loads[i][key]) + ' MW'))

        self.generator_load_table.resizeColumnsToContents()


    def update_generator_cost_table(self, generator_costs):
        self.generator_cost_table.setRowCount(len(generator_costs))
        self.generator_cost_table.setColumnCount(len(generator_costs[0]))

        self.generator_cost_table.setHorizontalHeaderLabels(list(generator_costs[0].keys()))

        keys = list(generator_costs[0].keys())

        for i in range(len(generator_costs)):
            for j in range(len(generator_costs[0])):
                key = keys[j]
                self.generator_cost_table.setItem(i, j, QTableWidgetItem(str(generator_costs[i][key]) + ' $'))

        self.generator_cost_table.resizeColumnsToContents()


    def update_generator_co2_emission_table(self, generator_co2_emissions):
        self.generator_co2_emission_table.setRowCount(len(generator_co2_emissions))
        self.generator_co2_emission_table.setColumnCount(len(generator_co2_emissions[0]))

        self.generator_co2_emission_table.setHorizontalHeaderLabels(list(generator_co2_emissions[0].keys()))

        keys = list(generator_co2_emissions[0].keys())

        for i in range(len(generator_co2_emissions)):
            for j in range(len(generator_co2_emissions[0])):
                key = keys[j]
                self.generator_co2_emission_table.setItem(i, j, QTableWidgetItem(str(generator_co2_emissions[i][key]) + ' ton'))

        self.generator_co2_emission_table.resizeColumnsToContents()