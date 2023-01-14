import json

from load_optimization.enum.generator_enum import GeneratorType

class JsonHelper():
    def __init__(self) -> None:
        pass


    def save_generator_as_json(self, generator, file_name):
        generator_dict = vars(generator)

        generator_json = json.dumps(generator_dict)

        with open(f"{file_name}.json", "w") as file:
            file.write(generator_json)


    def load_generator_as_json(self, file_name):
        generator_dict = {}

        with open(f"{file_name}.json", "r") as file:
            generator_dict = json.load(file)

        generator_dict['generator_type'] = GeneratorType(generator_dict['generator_type'])

        return generator_dict