import numpy as np
import pandas as pd
import sudoku_tools as sutils
import genetic_functions as genutils
from sudoku_genetic import SudokuGeneticAlgorithm
import multiprocessing as mp

# -------------------- Simulation --------------------


def run_simulation(test_board, generations):

    start = np.array(test_board['board_input'])
    gen_alg = SudokuGeneticAlgorithm(start)

    # print(gen_alg.initial_board)

    # add objectives
    gen_alg.add_fitness('row conflicts', genutils.row_conflicts)
    gen_alg.add_fitness('column conflicts', genutils.col_conflicts)
    gen_alg.add_fitness('box conflicts', genutils.box_conflicts)
    # gen_alg.add_fitness('total conflicts', genutils.total_conflicts)

    gen_alg.add_agent('row swap', genutils.shuffle_row, 0.6)
    gen_alg.add_agent('greedy row swap', genutils.greedy_shuffle_row, 0.4)

    # CHANGE TO 300
    gen_alg.generate_samples(300)

    # evolve population
    board, conflicts, time = gen_alg.evolve(generations=generations,
                                            offspring_n=300,
                                            elite_n=10)

    evo = gen_alg.evolution
    if len(evo) < generations + 1:
        evo += [evo[-1]] * (generations + 1 - len(evo))
    # print(board)
    # actual_sol = np.array(sutils.formatted_to_array(test_board['solution']))
    # print(actual_sol)
    # print(np.where(board == actual_sol, 1, 0))
    print('Simulation finished')
    return [time] + evo


def main():
    difficulties = ['easy', 'medium', 'hard']
    generations = 500
    evolutions = []
    output_csv_path = 'genetic_evolutions.csv'

    for diff in difficulties:
        print('---------------'+diff+'---------------')
        test_boards = sutils.get_test_boards(difficulty=diff, num_examples=50)

        workers = min(5, mp.cpu_count())

        try:
            with mp.Pool(processes=workers) as pool:
                args = [(tb, generations) for tb in test_boards]
                results = pool.starmap(run_simulation, args)
                results = map(lambda lst: [diff] + lst, results)
                evolutions += results
        except KeyboardInterrupt:
            print("Process interrupted, terminating simulations...")
            pool.terminate()
            pool.join()
            return

    evo_df = pd.DataFrame(evolutions, columns=['Difficulty', 'Time']+list(np.arange(generations+1)))
    evo_df.to_csv(output_csv_path)


if __name__ == '__main__':
    main()
