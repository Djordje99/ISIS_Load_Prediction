from sklearn.preprocessing import MinMaxScaler
import numpy as np
FUNCTION_RANGE = [20, 40, 60, 80, 100]


class GraphLinearization():
    def __init__(self) -> None:
        self.scaler = MinMaxScaler()

    def normalize_data(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))


    def get_consumption_linear_approximation(self, points, predicted_load, generator_percentage, generator_max_capacity_load, generator_min_capacity_load, generator_count):
        generator_predicted_load = predicted_load * generator_percentage

        single_generator_load = generator_predicted_load / generator_count

        generator_load_percentage = self.normalize_data([generator_min_capacity_load, single_generator_load, generator_max_capacity_load])

        coefficients = [1, 0]

        if generator_load_percentage[1] < 0.4:
            coefficients = np.polyfit([FUNCTION_RANGE[0], FUNCTION_RANGE[1]], [points[0], points[1]], 1)
        elif single_generator_load[1] < 0.6 and single_generator_load[1] > 0.4:
            coefficients = np.polyfit([FUNCTION_RANGE[1], FUNCTION_RANGE[2]], [points[1], points[2]], 1)
        elif single_generator_load[1] < 0.8 and single_generator_load[1] > 0.6:
            coefficients = np.polyfit([FUNCTION_RANGE[2], FUNCTION_RANGE[3]], [points[2], points[3]], 1)
        elif single_generator_load[1] < 1 and single_generator_load[1] > 0.8:
            coefficients = np.polyfit([FUNCTION_RANGE[3], FUNCTION_RANGE[4]], [points[3], points[4]], 1)

        return coefficients[0], coefficients[1]
