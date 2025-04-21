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
        self.evolution = []     # store best solution over generations
        self.fitness = {}   # name: func
        self.agents = {}    # name: func
        self.agent_weights = []     # weights for agent functions

    def add_fitness(self, func_name, func):
        self.fitness[func_name] = func

    def add_agent(self, func_name, func, w):
        self.agents[func_name] = func
        self.agent_weights.append(w)

    def add_sample(self, sample):
        ''' Evaluate fitness of sample and add to population '''
        scores = tuple([(key, func(sample)) for key, func in self.fitness.items()])
        value = {'eval': scores, 'total conflicts': sum(score for _, score in scores),
                 'board': sample}
        self.population[len(self.population)+1] = value

    def generate_samples(self, size):
        for _ in range(size):
            board = self.initial_board.copy()
            for i in range(len(board)):
                row = board[i]
                immutable_indices = np.where(row > 0)
                mutable_indices = np.where(row == 0)
                missing = list(set(np.arange(1, 10)) - set(row[immutable_indices]))
                new = np.random.choice(missing, size=len(missing), replace=False)
                row[mutable_indices] = new

            self.add_sample(board)

    def generate_random_samples(self, size):
        for _ in range(size):
            sample = np.where(self.initial_board == 0,
                              np.random.randint(1, 10, size=self.initial_board.shape),
                              self.initial_board)

            self.add_sample(sample)

    def get_top_k_solutions(self, k=1):
        sorted_items = sorted(self.population.items(), key=lambda item: item[1]['total conflicts'])
        top_k_items = sorted_items[:k]
        top_indices = [item[0] for item in top_k_items]
        top_evals = [item[1]['eval'] for item in top_k_items]
        top_conflicts = [item[1]['total conflicts'] for item in top_k_items]
        top_boards = [item[1]['board'] for item in top_k_items]
        return top_indices, top_evals, top_conflicts, top_boards

    def mutate(self, sample):
        ''' Mutate a random solution in current population with agent, add to population '''
        selected_agent = np.random.choice(list(self.agents.keys()), p=self.agent_weights)
        agent_func = self.agents[selected_agent]
        k = np.random.randint(2, 5)
        mutated = agent_func(sample, self.mutable, k)
        return mutated

    def crossover(self, parent1, parent2, mutation_rate=0.8):
        ''' Crossover population row-wise '''
        crossover_point = np.random.randint(0, 9)
        offspring = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))

        if np.random.randn() < mutation_rate:
            offspring = self.mutate(offspring)
        self.add_sample(offspring)

    def evolve(self, generations=500, offspring_n=300, elite_n=10, time_limit=900):
        ''' Evolve population, return solution board and time taken'''
        start_time = time.time()
        for i in range(generations):

            if time.time() - start_time > time_limit:
                break

            # elitism
            elite_indices, elite_evals, elite_conflicts, elite_boards = self.get_top_k_solutions(elite_n)
            self.evolution.append(elite_conflicts[0])

            # if i % 10 == 0:
            #     print(f"Best conflicts after {i}/{generations}: {elite_conflicts[0]}")
            #     print(f"Eval:{elite_evals[0]}\n")

            if elite_conflicts[0] == 0:
                print('Solved')
                return elite_boards[0], elite_conflicts[0], time.time() - start_time

            # renew population
            old_population = {k: v for k, v in self.population.items() if k not in elite_indices}
            self.population = {}
            for board in elite_boards:
                self.add_sample(board)

            for _ in range(offspring_n):
                # divisor = np.sum([1/v['total conflicts'] for v in old_population.values()])
                # weights = [(1/v['total conflicts'])/divisor for v in old_population.values()]
                old_keys = list(old_population.keys())
                conflicts = np.array([old_population[k]['total conflicts'] for k in old_keys])
                inv_conflicts = 1 / conflicts
                weights = inv_conflicts / inv_conflicts.sum()
                parent1_idx, parent2_idx = np.random.choice(old_keys, 2, p=weights)

                rnd = np.random.randn()
                if rnd < 0.1:
                    parent1 = elite_boards[np.random.choice(elite_n)]
                else:
                    parent1 = old_population[parent1_idx]['board']
                parent2 = old_population[parent2_idx]['board']
                self.crossover(parent1, parent2)

            if i != 0 and i % 50 == 0:
                self.generate_samples(int(offspring_n/3))

        best_indices, best_evals, best_conflicts, best_boards = self.get_top_k_solutions(1)
        self.evolution.append(best_conflicts[0])
        return best_boards[0], best_conflicts[0], time.time() - start_time
