import random
import numpy as np
import copy

from services.preprocessing.preparer import Preparer
from services.scorer.scrorer import Scorer
from services.training.ann_regression import AnnRegression

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.model_selection import train_test_split

SHARE_FOR_TRAINING = 0.85
ACCURACY_LEVEL = 20

class GeneticFeatureSelection():
    def __init__(self):
        self.scorer = Scorer()
        self.ann_regression = AnnRegression()
        self.preparer = Preparer(SHARE_FOR_TRAINING)
        self.data_frame = self.preparer.get_prepared_data_frame()
        self.X_feature_number = len(self.data_frame.columns) - 1


    def generate_random_individuals(self, num_individuals, max_features=None):
        """
        Randomly generates individuals
        The number of individuals to generate is given by the num_individuals parameter
        The length of each individual is equal to the num_features parameter
        The maximum number of active features for every individual is given by the max_features parameter
        """
        individuals = list()

        for _ in range(num_individuals):
            individual = ''
            for _ in range(self.X_feature_number):
                if individual.count('1') == max_features:
                    individual += '0'
                    continue

                individual += str(random.randint(0, 1))

            individuals.append(individual)

        return individuals


    def get_fitness_func(self, individual):
        """
        Calculate accuracy for the individual passed as parameter.
        Both the data_frame and the y_data parameters are used for training and evaluating the model.
        """
        X_train, y_train, X_test, y_test = self.preparer.prepare_for_training(individual)

        gen_feature_len = len(self.preparer.get_prepared_data_frame().columns) - 1

        print(f'\nWorking with {gen_feature_len} column number: \n{self.preparer.get_prepared_data_frame().columns}\n')

        y_pred = self.ann_regression.test_model(gen_feature_len, 3, X_train, y_train, X_test)

        accuracy = self.scorer.get_mean_absolute_percentage_error(y_test, y_pred)

        print(f'\nTest data: {accuracy}% MAPE\n')

        return accuracy


    def get_weights(self, population):
        """
        Calculate weights from the population filled with the accuracies
        """
        total_accuracies = 0
        new_population = []

        # Get the sum of all accuracies of the population
        for individual in population:
            total_accuracies += individual[1]

        # For each individual, calculate its weight by dividing its accuracy by the overall sum calculated above
        for individual in population:
            weight = individual[1]/total_accuracies
            # Store the individual and its weight in the final population list
            new_population.append((individual[0], float(weight*100)))

        return new_population


    def fill_population(self, individuals):
        """
        Fills the population list with individuals and their weights
        """
        population = list()

        for individual in individuals:
            # Get the value of the fitness function (accuracy of the model)
            accuracy = self.get_fitness_func(individual)

            # Check that the value is not the goal state (in this case, an accuracy of 80% is a terminal state)
            if float(accuracy) < ACCURACY_LEVEL:
                return individual

            individual_complete = (individual, accuracy)
            population.append(individual_complete)

        # The final population list is created, which contains each individual together with its weight
        # (weights will be used in the reproduction step)
        new_population = self.get_weights(population)

        return new_population


    def choose_parents(self, population, counter):
        """
        From the population, weighting the probabilities of an individual being chosen via the fitness
        function, takes randomly two individual to reproduce
        Population is a list of tuples, where the first element is the individual and the second
        one is the probability associated to it.
        To avoid generating repeated individuals, 'counter' parameter is used to pick parents in different ways, thus
        generating different individuals
        """
        # Pick random parent Number 1 and Number 2
        # (get_n_individual() function randomly picks an individual following the distribution of the weights)
        if counter == 0:
            parent_1 = self.get_n_individual(0, population)
            parent_2 = self.get_n_individual(1, population)
        elif counter == 1:
            parent_1 = self.get_n_individual(0, population)
            parent_2 = self.get_n_individual(2, population)

        else:
            probabilities = (individual[1] for individual in population)
            individuals = [individual[0] for individual in population]
            parent_1, parent_2 = random.choices(individuals, weights=probabilities, k=2)

        return [parent_1, parent_2]


    def get_n_individual(self, counter, population):
        """
        If counter is 0, return the individual with the highest prob
        If counter is 1, return the second individual with the highest prob
        If counter is 2, return the third individual withthe highest prob
        """
        index = counter + 1
        probabilities = [ind[1] for ind in population]
        sorted_probs = sorted(probabilities, key=float)
        max_prob = probabilities[-index]
        max_individual = [ind[0] for ind in population if ind[1] == max_prob][0]

        return max_individual


    def mutate(self, child, prob=0.1):
        """
        Randomly mutates an individual according to the probability given by prob parameter
        """
        new_child = copy.deepcopy(child)
        for i, char in enumerate(new_child):
            if random.random() < prob:
                new_value = '1' if char == '0' else '0'
                new_child = new_child[:i] + new_value + new_child[i+1:]

        return new_child


    def reproduce(self, individual_1, individual_2):
        """
        Takes 2 individuals, and combines their information based on a
        randomly chosen crosspoint.
        Each reproduction returns 2 new individuals
        """
        # Randomly generate a integer between 1 and the length of the individuals minus one, which will be the crosspoint
        crosspoint = random.randint(1, len(individual_1)-1)
        child_1 = individual_1[:crosspoint] + individual_2[crosspoint:]
        child_2 = individual_2[:crosspoint] + individual_1[crosspoint:]
        child_1, child_2 = self.mutate(child_1), self.mutate(child_2)

        return [child_1, child_2]


    def generation_ahead(self, population):
        """
        Reproduces all the steps for choosing parents and making
        childs, which means creating a new generation to iterate with
        """
        new_population = list()

        for _ in range(int(len(population)//2)):
            # According to the weights calculated before, choose a set of parents to reproduce
            parents = self.choose_parents(population, counter=_)

            # Reproduce the pair of individuals chose above to generate two new individuals
            childs = self.reproduce(parents[0], parents[1])

            new_population += childs

        return new_population


    def run_genetic_selection(self, num_individuals, max_iter=3):
        """
        Performs all the steps of the Genetic Algorithm
        1. Generate random population
        2. Fill population with the weights of each individual
        3. Check if the goal state is reached
        4. Reproduce the population, and create a new generation
        5. Repeat process until termination condition is met
        """
        # Generate individuals (returns a list of strings, where each str represents an individual)
        individuals = self.generate_random_individuals(num_individuals)

        # Returns a list of tuples, where each tuple represents an individual and its weight
        population = self.fill_population(individuals)

        # Check if a goal state is reached
        # When goal state is reached, fill_population() function returns a str, otherwise continue
        if isinstance(population, str):
            return population

        # Reproduce current generation to generate a better new one
        new_generation = self.generation_ahead(population)

        # After the new generation is generated, the loop goes on until a solution is found or until the maximum number of
        # iterations are reached
        iteration_count = 0
        while iteration_count < max_iter:
            population = self.fill_population(new_generation)

            # Check if a goal state is reached
            if isinstance(population, str):
                break

            new_generation = self.generation_ahead(population)
            iteration_count += 1

        return population
