import sudoku_tools as sutils
import numpy as np
from functools import reduce
import copy
import time


class SudokuGeneticAlgorithm:

    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.mutable = list(zip(*np.where(self.initial_board == 0)))   # list of indices of mutable positions
        self.population = {}    # potential solution array, scores: board
        self.fitness = {}   # name: func
        self.agents = {}    # name: func

    def add_fitness(self, func_name, func):
        self.fitness[func_name] = func

    def add_agent(self, func_name, func):
        self.agents[func_name] = func

    def add_sample(self, sample):
        ''' Evaluate fitness of sample and add to population'''
        scores = tuple([(key, func(sample)) for key, func in self.fitness.items()])
        self.population[scores] = sample

    def get_sample(self):
        ''' Get random sample from current population '''
        idx = np.random.choice(len(self.population.values()))
        sample = list(self.population.values())[idx]
        return copy.deepcopy(sample)

    def get_best_solution(self):
        total_scores = [key[3][1] for key in self.population.keys()]
        best_eval, best_sol = list(self.population.items())[np.argmin(total_scores)]
        return best_eval, best_sol

    @staticmethod
    def _dominates(p, q):
        ''' Checks whether one solution (p) dominates another (q) '''
        score_diffs = [y - x for (_, x), (_, y) in zip(p, q)]
        return min(score_diffs) >= 0.0 and max(score_diffs) > 0.0

    @staticmethod
    def _reduce_population(solutions, p):
        return solutions - {q for q in solutions if SudokuGeneticAlgorithm._dominates(p, q)}

    def remove_dominated(self):
        non_dominated = reduce(SudokuGeneticAlgorithm._reduce_population,
                               self.population.keys(), self.population.keys())
        self.population = {key: self.population[key] for key in non_dominated}

    def mutate(self, agent_name):
        ''' Mutate a random solution in current population with agent '''
        agent_func = self.agents[agent_name]
        sample = self.get_sample()
        mutated = agent_func(sample, self.mutable)
        self.add_sample(mutated)

    def crossover(self, parent1, parent2):
        ''' Crossover population '''
        crossover_point = np.random.randint(0, 9)
        offspring = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))

        # agent_keys = list(self.agents.keys())
        # selected_agent = np.random.choice(agent_keys)
        # agent_func = self.agents[selected_agent]
        # mutated = agent_func(offspring, self.mutable)
        self.add_sample(offspring)

    def evolve(self, num_iter=100000, selection_period=150, crossover_point=200, time_limit=600):
        ''' Evolve population '''
        start_time = time.time()
        agent_keys = list(self.agents.keys())

        for i in range(num_iter):
            if time.time() - start_time >= time_limit:
                break

            selected_agent = np.random.choice(agent_keys)
            if i > 5000:
                rnd = np.random.randn()
                if rnd < 0.5:
                    selected_agent = 'shuffle boxes'

            self.mutate(selected_agent)

            if i % crossover_point == 0:
                for _ in range(50):
                    parent1 = self.get_sample()
                    parent2 = self.get_sample()
                    self.crossover(parent1, parent2)

            if i > 0 and i % selection_period == 0:
                self.remove_dominated()
                best_eval, best_sol = self.get_best_solution()
                if best_eval[3][1] == 0:
                    break
                if i % 1000 == 0:
                    print(best_eval)

            if i % 1000 == 0:
                print(f'{i}/{num_iter}')
                print(f'Population size: {len(self.population)}')

        print('Evolution finished')
        self.remove_dominated()
