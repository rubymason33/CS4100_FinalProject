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
