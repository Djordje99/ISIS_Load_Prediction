from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class OptimizeTab():
    def __init__(self, tab:QWidget) -> None:
        self.cost_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'cost_weighted_factor_spin_box')
        self.co2_weighted_factor_spin_box: QDoubleSpinBox = tab.findChild(QDoubleSpinBox, 'co2_weighted_factor_spin_box')
        self.generator_table:QTableWidget = tab.findChild(QTableWidget, 'generator_table')

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


    def update_table(self, result):
        self.generator_table.setRowCount(len(result))
        self.generator_table.setColumnCount(len(result[0]))

        self.generator_table.setHorizontalHeaderLabels(list(result[0].keys()))

        keys = list(result[0].keys())

        for i in range(len(result)):
            for j in range(len(result[0])):
                key = keys[j]
                self.generator_table.setItem(i, j, QTableWidgetItem(str(result[i][key])))

        self.generator_table.resizeColumnsToContents()