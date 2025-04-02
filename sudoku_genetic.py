import sudoku_tools as sutils


class SudokuGeneticAlgorithm:

    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.mutable = []   # list of indices of mutable positions
        self.population = {}    # potential solution array
        self.fitness = {}   # name: func
        self.agents = {}    # name: func

    def add_fitness(self, func_name, func):
        pass

    def add_agent(self, func_name, func):
        pass
