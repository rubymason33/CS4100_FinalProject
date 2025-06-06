import pandas as pd

EASY_PATH = 'sudoku_datasets/sudoku_easy.csv'
MED_PATH = 'sudoku_datasets/sudoku_medium.csv'
HARD_PATH = 'sudoku_datasets/sudoku_hard.csv'


def display_board(board: str) -> str:
    """Get the board from the csv file version (string)

    Args:
        board (str): the board as a string representation

    Returns:
        str: a formatted string of the board
    """
    split_board = list(board)
    board_str = ""
    for i in range(9):
        row = split_board[i*9:(i+1)*9]
        board_str += ' '.join(row[0:3]) + ' | ' + ' '.join(row[3:6]) + ' | ' + ' '.join(row[6:9]) + '\n'
        if i in [2, 5]:
            board_str += '-' * 21 + '\n'
    return board_str

def get_board_details(board_details: pd.Series) -> tuple:
    """Gets the details for a specified row of the csv

    Args:
        board_details (pd.Series): the row of the csv

    Returns:
        tuple: the different details in a formatted way
    """
    board = board_details['puzzle']
    solution = board_details['solution']
    num_clues = board_details['clues']
    difficulty_rating = board_details['difficulty']

    # get the rendered version
    board = display_board(board)
    solution = display_board(solution)
    
    return board, solution, num_clues, difficulty_rating

def formatted_to_array(formatted_str: str) -> list:
    """Turns the string representation into an array of ints that can be read by the algorithms

    Args:
        formatted_str (str): the string representation

    Returns:
        list: data as an array of ints
    """
    rows = formatted_str.strip().split('\n')
    board_2d = []

    for row in rows:
        if '-' in row:
            continue
        clean_row = row.replace('|', '').strip().split()
        int_row = [0 if cell == '.' else int(cell) for cell in clean_row]
        board_2d.append(int_row)

    return board_2d

def array_to_formatted(board_2d: list) -> str:
    """Converts (solved) array back to a string

    Args:
        board_2d (list): board as an array of ints

    Returns:
        str: formatted string representation for reading
    """
    board_str = ""
    for i, row in enumerate(board_2d):
        display_row = [str(cell) if cell != 0 else '.' for cell in row]
        board_str += ' '.join(display_row[:3]) + ' | ' + ' '.join(display_row[3:6]) + ' | ' + ' '.join(display_row[6:]) + '\n'
        if i in [2, 5]:
            board_str += '-' * 21 + '\n'
    return board_str

def get_test_boards(difficulty: str, num_examples: int=10) -> list:
    """Get a specified number of boards under a difficulty

    Args:
        difficulty (str): easy, medium, or hard
        num_examples (int, optional): Number of boards to fetch. Defaults to 10.

    Returns:
        list: list of dictionaries containing all the information for each sampled board
    """
    if difficulty.lower() == 'easy':
        path = EASY_PATH
    elif difficulty.lower() == 'medium':
        path = MED_PATH
    elif difficulty.lower() == 'hard':
        path = HARD_PATH
    else:
        print('Please give one of the following difficulties: "easy", "medium", "hard"')
        return []
    
    boards_data = []
    
    df = pd.read_csv(path)
    sampled_boards = df.sample(n=num_examples, replace=False)

    for _, board_row in sampled_boards.iterrows():
        board, solution, num_clues, difficulty_rating = get_board_details(board_row)
        board_input = formatted_to_array(board)
        
        one_board_data = {
            'board': board,
            'board_input': board_input,
            'solution': solution,
            'num_clues': num_clues,
            'difficulty_rating': difficulty_rating
        }
        
        boards_data.append(one_board_data)

    return boards_data

def check_solution(generated_sol: list, actual_sol: list) -> tuple:
    """Checks if solution is the same as the provided answer

    Args:
        generated_sol (list): 2d representation of generated board
        actual_sol (list): 2d representation of provided board

    Returns:
        tuple: the percent and number correct
    """
    num_correct = 0
    for row_gen, row_act in zip(generated_sol, actual_sol):
        for val_gen, val_act in zip(row_gen, row_act):
            if val_gen == val_act:
                num_correct += 1
            
    percent_correct = num_correct/81
    
    return percent_correct, num_correct

def is_valid_sequence(sequence: list) -> bool:
    """Check if a sequence is valid

    Args:
        sequence (list): a list of ints ranging from 1-9

    Returns:
        bool: if the sequence is unique 1-9 (valid sudoku)
    """
    all_nums = set(range(1,10))
    current_sequence = set(sequence)
    
    return current_sequence == all_nums

def is_valid_board(board: list) -> bool:
    """Checks if board is a valid sudoku solution

    Args:
        board (list): a 2d list of ints representing the board

    Returns:
        bool: if the board is a valid solution
    """
    all_rows = True
    all_cols = True
    all_cells = True
    
    rows = [row for row in board]
    cols = []
    cells = []
    
    # get the cols
    for i in range(9):
        col = []
        for row in board:
            col.append(row[i])
        cols.append(col)
        
    # get the cells
    for cell_row in range(0, 9, 3):
        for cell_col in range(0, 9, 3):
            cell = []
            for i in range(3):
                for j in range(3):
                    cell.append(board[cell_row + i][cell_col + j])
            cells.append(cell)
            
    # check all the rows
    for row in rows:
        if not is_valid_sequence(row):
            all_rows = False
            break

    # check all the cols
    for col in cols:
        if not is_valid_sequence(col):
            all_cols = False
            break

    # check all the cells
    for cell in cells:
        if not is_valid_sequence(cell):
            all_cells = False
            break
        
    return all([all_rows, all_cols, all_cells])

def is_currently_valid_sequence(sequence: list) -> bool:
    """Check if a sequence is currently valid

    Args:
        sequence (list): a list of ints ranging from 1-9

    Returns:
        bool: if the sequence is unique 1-9 (valid sudoku)
    """
    filled_nums = [num for num in sequence if num !=0]
    no_dups = set(filled_nums)
    
    return len(no_dups) == len(filled_nums)

def is_currently_valid_board(board: list) ->bool:
    """Checks if board is currently a valid sudoku solution

    Args:
        board (list): a 2d list of ints representing the board

    Returns:
        bool: if the board is a valid solution
    """
    all_rows = True
    all_cols = True
    all_cells = True
    
    rows = [row for row in board]
    cols = []
    cells = []
    
    # get the cols
    for i in range(9):
        col = []
        for row in board:
            col.append(row[i])
        cols.append(col)
        
    # get the cells
    for cell_row in range(0, 9, 3):
        for cell_col in range(0, 9, 3):
            cell = []
            for i in range(3):
                for j in range(3):
                    cell.append(board[cell_row + i][cell_col + j])
            cells.append(cell)
            
    # check all the rows
    for row in rows:
        if not is_currently_valid_sequence(row):
            all_rows = False
            break

    # check all the cols
    for col in cols:
        if not is_currently_valid_sequence(col):
            all_cols = False
            break

    # check all the cells
    for cell in cells:
        if not is_currently_valid_sequence(cell):
            all_cells = False
            break
        
    return all([all_rows, all_cols, all_cells])




def main():
    # df = pd.read_csv(EASY_PATH)

    # test = df.iloc[0,:]
    # board, solution, num_clues, difficulty_rating = get_board_details(test)
    # print('board:')
    # print(board)
    # print('solution:')
    # print(solution)
    
    # print('testing formatting for solving algorithms...')
    # board_as_array = formatted_to_array(board)
    # board_as_string = array_to_formatted(board_as_array)
    # print('array:')
    # print(board_as_array)
    # print('getting item [4,6]')
    # print(board_as_array[4][6])
    # print('formatted:')
    # print(board_as_string)
    # test = get_test_boards('easy', 2)
    # print(test[0]['board_input'])
    pass


if __name__ == "__main__":
    main()

    
    
    
    
