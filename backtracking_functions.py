"""
Functions for the backtracking algorithm
"""

import sudoku_tools as sutils
import random
import pprint

class Backtracking():
    def __init__(self, board:list):
        self.board = board
    
    def get_empty(self) -> tuple:
        """Get the first empty cell

        Returns:
            tuple: the row and col of the empty cell
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None # all full
        
    def get_valid_numbers(self, row: int, col: int) -> list:
        """Get all the numbers that are valid options for a specific cell

        Args:
            row (int): index of row
            col (int): index of col

        Returns:
            list: all the valid numbers that can be placed here
        """
        used = set()
        
        # add all in row
        used.update(self.board[row])
        
        # add all in col
        used.update([self.board[i][col] for i in range(9)])
        
        # get the top corner of the 3x3 box
        box_start_row = 3 * (row // 3)
        box_start_col = 3 * (col // 3)
        
        # add all the 3x3 vals
        for i in range(3):
            for j in range(3):
                used.add(self.board[box_start_row + i][box_start_col + j])
                
        options = [num for num in range(1, 10) if num not in used]
        return options
    
    def get_most_conflicts_cell(self) -> tuple:
        """get the cell that has the most conflicts/constraints on what number can be placed

        Returns:
            tuple: the cell row and col
        """
        min_options = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    options = self.get_valid_numbers(i, j)
                    
                    if  len(options) < min_options:
                        min_options = len(options)
                        best_cell = (i, j) # set this to be the most constrained cell
                        
                        if min_options == 1: # only one number can be placed here
                            return best_cell
        return best_cell

    # def solve(self) -> list:
    #     """solve the given sudoku

    #     Returns:
    #         list: the solved board as a 2d array
    #     """
    #     empty = self.get_empty()
    #     if not empty:
    #         return self.board
        
    #     row, col = empty
        
    #     for num in range(1, 10):
    #         self.board[row][col] = num
            
    #         if sutils.is_currently_valid_board(self.board):
    #             if self.solve():
    #                 return self.board
                
    #         self.board[row][col] = 0 # set back as empty
            
    def solve(self) -> list:
        """solve the given sudoku,a nd using the updated heuristic

        Returns:
            list: the solved board as a 2d array
        """
        empty = self.get_most_conflicts_cell()
        if not empty:
            return self.board
        
        row, col = empty
        
        # get the numbers that can be placed here
        options = self.get_valid_numbers(row, col)
        for num in options:
            self.board[row][col] = num
            
            if sutils.is_currently_valid_board(self.board):
                if self.solve(): # recursive call
                    return self.board
                
            self.board[row][col] = 0 # set back as empty, backtrack
            
        return None # unsolved
            
def main():
    # test_invalid_blanks = [0, 1, 4, 5, 7, 4, 0, 8, 9]
    # test_valid_blanks = [0, 0, 0, 1, 5, 7, 8, 9, 0]
    # print('invalid:', is_currently_valid_sequence(test_invalid_blanks))
    # print('valid:', is_currently_valid_sequence(test_valid_blanks))
    
    # test_invalid = [[0, 5, 7, 2, 5, 4, 9, 8, 1],
    #                 [8, 2, 4, 9, 3, 1, 0, 5, 0],
    #                 [9, 1, 6, 0, 5, 7, 2, 3, 4],
    #                 [2, 0, 8, 0, 4, 6, 3, 0, 5],
    #                 [1, 9, 9, 5, 2, 3, 8, 7, 6],
    #                 [0, 3, 5, 0, 8, 9, 4, 1, 2],
    #                 [5, 6, 2, 3, 7, 8, 1, 1, 9],
    #                 [4, 9, 0, 6, 1, 5, 7, 0, 8],
    #                 [7, 0, 1, 4, 0, 2, 5, 6, 3]]
    # test_valid_small =  [[0, 5, 7, 2, 6, 4, 9, 8, 1],
    #             [8, 2, 4, 9, 3, 1, 6, 5, 7],
    #             [9, 1, 6, 8, 5, 7, 2, 3, 4],
    #             [2, 7, 8, 1, 4, 6, 3, 9, 5],
    #             [1, 4, 9, 5, 2, 3, 8, 7, 6],
    #             [6, 3, 5, 7, 8, 9, 4, 1, 2],
    #             [5, 6, 2, 3, 7, 8, 1, 4, 9],
    #             [4, 9, 3, 6, 1, 5, 7, 2, 8],
    #             [7, 8, 1, 4, 9, 2, 5, 6, 3]]
    
    # test_valid_big =  [[3, 5, 7, 2, 6, 4, 9, 0, 1],
    #         [8, 2, 4, 9, 3, 1, 6, 5, 7],
    #         [0, 1, 0, 8, 5, 0, 2, 0, 4],
    #         [2, 7, 8, 1, 4, 6, 3, 9, 5],
    #         [1, 4, 0, 5, 2, 0, 8, 7, 6],
    #         [6, 0, 0, 7, 8, 9, 4, 1, 2],
    #         [5, 6, 2, 3, 7, 0, 1, 4, 9],
    #         [0, 9, 3, 6, 1, 5, 7, 2, 8],
    #         [7, 0, 1, 0, 9, 2, 5, 6, 3]]
    
    # # print('invalid:', sutils.is_currently_valid_board(test_invalid))
    # # print('valid:', sutils.is_currently_valid_board(test_valid))
    
    # test = Backtracking(test_valid_big)
    # sol = test.solve()
    # pprint.pp(sol)
    pass

if __name__ == "__main__":
    main()