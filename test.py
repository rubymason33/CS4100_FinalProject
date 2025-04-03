import sudoku_tools as sutils
import pandas as pd
import pprint

print('Testing calling the sudoku utils file!')

print('Let\'s get 5 random boards for our algorithm:')
test_boards = sutils.get_test_boards(difficulty='easy', num_examples=5)
print('Each board has a dict with information. Let\'s look at the first one:')
test_example = test_boards[0]
pprint.pp(test_example)

print('The data that we will pass into each algorithm is a 2D list:')
pprint.pp(test_example['board_input'])


print('Somewhere we will need to convert the generated answer into a readable format:')
print('We can use the array_to_formatted fn. Not sure if this will be the answer that the algorithm gives us?')
print('Pretend that the board input is our output for the sake of the fn demo')
to_string = sutils.array_to_formatted(test_example['board_input'])
print(to_string)


print('We also may need to convert the solution board into the array format so we can check if the algorithm did a good job')
to_array = sutils.formatted_to_array(test_example['solution'])
pprint.pp(to_array)


print('Let\'s check how many are correct between two different solutions')
print('For this we pretend that these are the algorithms generated sols')
generated_sol = sutils.formatted_to_array(test_boards[0]['solution'])
actual_sol1 = sutils.formatted_to_array(test_boards[0]['solution'])
actual_sol2 = sutils.formatted_to_array(test_boards[1]['solution'])

pct_diff, num_diff = sutils.check_solution(generated_sol=generated_sol, actual_sol=actual_sol2)
pct_same, num_same = sutils.check_solution(generated_sol=generated_sol, actual_sol=actual_sol1)

print(f'percent correct for differnt sols: {pct_diff*100:.2f}%,'
      f'\nnumber correct for differnt sols: {num_diff}')
print(f'percent correct for same sols: {pct_same*100:.2f}%,'
      f'\nnumber correct for same sols: {num_same}')

print('test if board is currently valid (ignore 0s)')
test_invalid = [[0, 5, 7, 2, 5, 4, 9, 8, 1],
              [8, 2, 4, 9, 3, 1, 0, 5, 0],
              [9, 1, 6, 0, 5, 7, 2, 3, 4],
              [2, 0, 8, 0, 4, 6, 3, 0, 5],
              [1, 9, 9, 5, 2, 3, 8, 7, 6],
              [0, 3, 5, 0, 8, 9, 4, 1, 2],
              [5, 6, 2, 3, 7, 8, 1, 1, 9],
              [4, 9, 0, 6, 1, 5, 7, 0, 8],
              [7, 0, 1, 4, 0, 2, 5, 6, 3]]
test_valid =  [[3, 5, 7, 2, 6, 4, 9, 8, 0],
             [8, 0, 4, 0, 3, 1, 6, 5, 7],
             [9, 1, 6, 8, 0, 7, 2, 0, 4],
             [2, 7, 8, 1, 4, 6, 3, 9, 5],
             [1, 4, 0, 5, 2, 3, 8, 7, 6],
             [6, 3, 5, 7, 8, 9, 0, 1, 2],
             [0, 6, 2, 0, 7, 8, 1, 4, 9],
             [4, 9, 3, 6, 1, 5, 7, 2, 8],
             [7, 8, 1, 4, 0, 2, 5, 6, 3]]

print('invalid:', sutils.is_currently_valid_board(test_invalid))
print('valid:', sutils.is_currently_valid_board(test_valid))

# print('Let\'s use the other functions to check if a board is correct\n'
#       'used for the algorithms and also if there is a valid solution that doesnt match the provided one')
# false_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
#                 [2, 3, 4, 5, 6, 7, 8, 9, 1],
#                 [3, 4, 5, 6, 7, 8, 9, 1, 2],
#                 [4, 5, 6, 7, 8, 9, 1, 2, 3],
#                 [5, 6, 7, 8, 9, 1, 2, 3, 4],
#                 [6, 7, 8, 9, 1, 2, 3, 4, 5],
#                 [7, 8, 9, 1, 2, 3, 4, 5, 6],
#                 [8, 9, 1, 2, 3, 4, 5, 6, 7],
#                 [9, 1, 2, 3, 4, 5, 6, 7, 8]]
# valid_board = [[3, 5, 7, 2, 6, 4, 9, 8, 1],
#                 [8, 2, 4, 9, 3, 1, 6, 5, 7],
#                 [9, 1, 6, 8, 5, 7, 2, 3, 4],
#                 [2, 7, 8, 1, 4, 6, 3, 9, 5],
#                 [1, 4, 9, 5, 2, 3, 8, 7, 6],
#                 [6, 3, 5, 7, 8, 9, 4, 1, 2],
#                 [5, 6, 2, 3, 7, 8, 1, 4, 9],
#                 [4, 9, 3, 6, 1, 5, 7, 2, 8],
#                 [7, 8, 1, 4, 9, 2, 5, 6, 3]]
    

# print('false board:', sutils.is_valid_board(false_board))
# print('valid board:', sutils.is_valid_board(valid_board))
