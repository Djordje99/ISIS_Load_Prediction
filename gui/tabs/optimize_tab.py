#from gui.load_prediction_controller import LoadPredictionController

class OptimizeTab():
    def __init__(self, window) -> None:
        self.window = window
        self.window.optimize_btn.clicked.connect(self.optimize)


    def optimize(self):
        max_power, min_power, coal_cost, power_plant_count, coal_consumption, co2_emission = self.window.coal_generator_tab.get_coal_generator_data()