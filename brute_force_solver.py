import time
import numpy as np
import random

def validator(board, row, col, num):
    # Check row and column
    if num in board[row] or num in board[:, col]:
        return False
    
    # Check sub-grid
    subgrid_row, subgrid_col = (row // 3) * 3, (col // 3) * 3 
    if num in board[subgrid_row:subgrid_row+3, subgrid_col:subgrid_col+3]:
        return False
    
    return True

def find_empty_cell(board):
    for r in range(9):
        for c in range(9):
            if board[r, c] == 0:
                return r, c
    return None

def sudoku_brute_force(board, start_time=None, time_limit=10):
    # Set start_time only once for the entire recursion
    if start_time is None:
        start_time = time.perf_counter()
    
    # Check if the time limit has been exceeded.
    if time.perf_counter() - start_time > time_limit:
        return False, board

    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return True, board  # Board is completely filled

    row, col = empty_cell
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if validator(board, row, col, num):
            board[row, col] = num
            solved, result = sudoku_brute_force(board, start_time, time_limit)
            if solved:
                return True, result
            board[row, col] = 0  # Backtrack

    return False, board  # No solution found

if __name__ == '__main__':
    # Test/demo code that runs only when executing this file directly.
    board = np.zeros((9, 9), dtype=int)
    
    # Optionally, set up an initial board here.
    # For example: board[0, 0] = 5, board[0, 1] = 3, etc.
    
    solved, solved_board = sudoku_brute_force(board)
    if solved:
        print("Solved Sudoku board:")
        print(solved_board)
    else:
        print("No solution exists for the provided board or time limit exceeded.")
