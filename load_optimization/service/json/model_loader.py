from load_optimization.service.json.helper import JsonHelper

from load_optimization.generator_model.thermal import ThermalGenerator
from load_optimization.generator_model.hydro import HydroGenerator
from load_optimization.generator_model.wind import WindGenerator
from load_optimization.generator_model.solar import SolarGenerator


class ModelLoader(JsonHelper):
    coal_generator = None
    gas_generator = None
    hydro_generator = None
    wind_generator = None
    solar_generator = None

    def __init__(self) -> None:
        super(ModelLoader, self).__init__()

    @staticmethod
    def get_coal_generator():
        return ModelLoader.coal_generator

    @staticmethod
    def get_gas_generator():
        return ModelLoader.gas_generator

    @staticmethod
    def get_hydro_generator():
        return ModelLoader.hydro_generator

    @staticmethod
    def get_wind_generator():
        return ModelLoader.wind_generator

    @staticmethod
    def get_solar_generator():
        return ModelLoader.solar_generator


    def load_models(self):
        ModelLoader.coal_generator = ThermalGenerator(**self.load_generator_as_json('D:\Fax\ISIS_Load_Prediction\load_optimization\service\json\json_model\coal_generator'))
        ModelLoader.gas_generator = ThermalGenerator(**self.load_generator_as_json('D:\Fax\ISIS_Load_Prediction\load_optimization\service\json\json_model\gas_generator'))
        ModelLoader.hydro_generator = HydroGenerator(**self.load_generator_as_json('D:\Fax\ISIS_Load_Prediction\load_optimization\service\json\json_model\hydro_generator'))
        ModelLoader.wind_generator = WindGenerator(**self.load_generator_as_json('D:\Fax\ISIS_Load_Prediction\load_optimization\service\json\json_model\wind_generator'))
        ModelLoader.solar_generator = SolarGenerator(**self.load_generator_as_json('D:\Fax\ISIS_Load_Prediction\load_optimization\service\json\json_model\solar_generator'))