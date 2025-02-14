import numpy as np
import random

def validator(board, row, col, num):
    subgrid_index = (row // 3) * 3 + (col // 3)  # Map cell to sub-grid
    
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

def solve(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # Board is completely filled
    
    row, col = empty_cell
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    
    for num in numbers:
        if validator(board, row, col, num):
            board[row, col] = num
            if solve(board):
                print(board)
                return True
            board[row, col] = 0  # Backtrack
    
    return False  # No solution found

# Initialize an empty Sudoku grid
sudoku_grid = np.zeros((9, 9), dtype=int)
print(solve(sudoku_grid))

