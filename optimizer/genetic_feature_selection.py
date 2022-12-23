import random
import numpy as np
import copy

from services.preprocessing.preparer import Preparer
from services.scorer.scrorer import Scorer


from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.model_selection import train_test_split

SHARE_FOR_TRAINING = 0.85

class GeneticFeatureSelection():
    def __init__(self):
        self.scorer = Scorer()


    def generate_random_individuals(self, num_individuals, num_features, max_features=None, verbose=False):
        """
        Randomly generates individuals
        The number of individuals to generate is given by the num_individuals parameter
        The length of each individual is equal to the num_features parameter
        The maximum number of active features for every individual is given by the max_features parameter
        """
        if verbose: print('GENERATING RANDOM INDIVIDUALS.... ')

        individuals = list()

        for _ in range(num_individuals):
            individual = ''
            for col in range(num_features):
                # For each char in the individual, a 1 or a 0 is randomly generated
                if individual.count('1') == max_features:
                    individual += '0'
                    continue

                individual += str(random.randint(0, 1))

            if verbose: print(f'Genrated a new indivudal: {individual}')

            individuals.append(individual)

        if verbose: print(f'Generated list of {num_individuals} individuals: {individuals}')

        return individuals


    def get_fitness_func(self, individual, data_frame, verbose=False):
        """
        Calculate accuracy for the individual passed as parameter.
        Both the data_frame and the y_data parameters are used for training and evaluating the model.
        """
        if verbose: print('Calculating accuracy for individual ', individual)

        # generate_data_frames_for_training() function splits a given dataset into training and test data,
        # and separates labels and rest of features
        y_data = data_frame['load']
        X_data = data_frame.drop('load', axis=1)

        print(X_data)
        print()
        print(y_data)

        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.25, random_state=42)

        X_train = X_train.loc[:, [True if individual[i] == '1' else False for i in range(len(individual))]]
        X_test = X_test.loc[:, [True if individual[i] == '1' else False for i in range(len(individual))]]

        model = self.create_model(X_train)

        X_train = np.asarray(X_train).astype(np.float64)
        X_test = np.asarray(X_test).astype(np.float64)
        y_train = np.asarray(y_train).astype(np.float64)
        y_test = np.asarray(y_test).astype(np.float64)

        print(X_test)

        model.fit(X_train, y_train, epochs=5, verbose=1 if verbose else 0)

        y_pred = model.predict(X_test)

        accuracy = self.scorer.get_mean_absolute_percentage_error(y_test, y_pred)

        if verbose: print(f"Accuracy for the classifier trained for individual {individual}: ", accuracy)

        return accuracy


    def create_model(self, X, verbose=False):
        """
        X: training dataset to be used. Its shape is used to set the input shape for the model.
        """
        model = Sequential()

        model.add(Dense(16, input_dim=X.shape[1], activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        if verbose: print('MODEL SUMMARY: \n')
        if verbose: print(model.summary())

        model.compile(loss='mean_squared_error', optimizer='nadam', metrics=['accuracy'])

        return model


    def generate_data_frames_for_training(self, data_frame, split_frac=0.8):
        """
        Generates training and testing data_frames from a complete data_frame, according to the split_frac parameter
        """

        train_data = data_frame.sample(frac=split_frac, random_state=314)
        test_data = data_frame.drop(train_data.index)

        X_train = train_data.loc[:, train_data.columns != 'Churn']
        X_test = test_data.loc[:, test_data.columns != 'Churn']
        y_train = train_data.loc[:, train_data.columns == 'Churn']
        y_test = test_data.loc[:, test_data.columns == 'Churn']

        print(X_train.shape)
        print(X_test.shape)
        print(y_train.shape)
        print(y_test.shape)

        return X_train, X_test, y_train, y_test


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

    def fill_population(self, individuals, data_frame, y_data, verbose=False):
        """
        Fills the population list with individuals and their weights
        """
        population = list()

        for individual in individuals:
            # Get the value of the fitness function (accuracy of the model)
            if verbose: print(f'Calculating fitness function value for individual {individual}')
            accuracy = self.get_fitness_func(individual, data_frame, verbose)

            # Check that the value is not the goal state (in this case, an accuracy of 80% is a terminal state)
            if float(accuracy) > 0.8:
                if verbose: print(f'Goal state found for individual {individual}')
                return individual

            individual_complete = (individual, accuracy)
            population.append(individual_complete)

        # The final population list is created, which contains each individual together with its weight
        # (weights will be used in the reproduction step)
        new_population = self.get_weights(population)
        if verbose: print(f'Generated population list (with weights): {new_population}')

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


    def generation_ahead(self, population, verbose=False):
        """
        Reproduces all the steps for choosing parents and making
        childs, which means creating a new generation to iterate with
        """
        new_population = list()

        for _ in range(int(len(population)//2)):
            # According to the weights calculated before, choose a set of parents to reproduce
            parents = self.choose_parents(population, counter=_)
            if verbose: print(f'Parents chosen: {parents}')

            # Reproduce the pair of individuals chose above to generate two new individuals
            childs = self.reproduce(parents[0], parents[1])
            if verbose: print(f'Generated children: {childs}\n')
            new_population += childs

        return new_population


    def run_genetic_selection(self, num_individuals, data_frame, max_iter=3, verbose=False):
        """
        Performs all the steps of the Genetic Algorithm
        1. Generate random population
        2. Fill population with the weights of each individual
        3. Check if the goal state is reached
        4. Reproduce the population, and create a new generation
        5. Repeat process until termination condition is met
        """
        # Generate individuals (returns a list of strings, where each str represents an individual)
        individuals = self.generate_random_individuals(num_individuals, len(data_frame.columns), verbose=verbose)

        print(data_frame)

        # Returns a list of tuples, where each tuple represents an individual and its weight
        population = self.fill_population(individuals, data_frame, verbose)

        # Check if a goal state is reached
        # When goal state is reached, fill_population() function returns a str, otherwise continue
        if isinstance(population, str):
            return population

        # Reproduce current generation to generate a better new one
        new_generation = self.generation_ahead(population, verbose)

        # After the new generation is generated, the loop goes on until a solution is found or until the maximum number of
        # iterations are reached
        iteration_count = 0
        while iteration_count < max_iter:
            if verbose: print(f'\n\n\nITERATION NUMBER {iteration_count+1} (Iteration max = {max_iter+1})\n\n\n')
            population = self.fill_population(new_generation, data_frame, verbose)

            # Check if a goal state is reached
            if isinstance(population, str):
                break

            new_generation = self.generation_ahead(population, verbose)
            iteration_count += 1

        return population
