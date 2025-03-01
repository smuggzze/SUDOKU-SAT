import numpy as np
import time
from brute_force_solver import sudoku_brute_force 
from sat_solver import sudoku_sat                  

def load_boards_from_txt(filename):
    """
    Input: file consisting of sudoku grids (currently 9x9 only compatible)
    Converts file contents to np arrays as neccessary
    Returns: list size x (depending on number of grids in file) list[type=np.array]
    """
    boards = []
    board_lines = []
    
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                board_lines.append(line.strip())
            else:
                if board_lines:
                    board = [list(map(int, row.split())) for row in board_lines]
                    boards.append(np.array(board))
                    board_lines = []
        if board_lines:
            board = [list(map(int, row.split())) for row in board_lines]
            boards.append(np.array(board))
    
    return boards

def print_board(board):
    """
    Input: np array of sudoku
    If neccessary converts board to np array
    Print: board as readable format
    """
    if isinstance(board, np.ndarray):
        board = board.tolist()
    for row in board:
        print(" ".join(str(num) for num in row))

def main():
    filename = 'sudoku_puzzles.txt'
    boards = load_boards_from_txt(filename)
    
    for i, board in enumerate(boards, start=1):
        print(f"Processing Board {i} with Brute Force Solver:")
        print("Original Board:")
        print_board(board)
        print()
        
        # Brute Force Solver
        start_time = time.time() * 1000
        solved, solved_board = sudoku_brute_force(board.copy())
        end_time = time.time() * 1000
        if solved:
            print(f"Brute Force took: {end_time - start_time} ms")
            print("Brute Force Solved Board:")
            print_board(solved_board)
        else:
            print("No solution exists for this board (Brute Force).")
        print("-" * 40)
        
        # SAT Solver
        print(f"Processing Board {i} with SAT Solver:")
        print("Original Board:")
        print_board(board)
        print()
        start_time = time.time() * 1000
        solved, solved_board = sudoku_sat(board.copy())
        end_time = time.time() * 1000
        if solved:
            print(f"SAT Solver took: {end_time - start_time} ms")
            print("SAT Solver Solved Board:")
            print_board(solved_board)
        else:
            print("No solution exists for this board (SAT Solver).")
        print("-" * 40)
        print()

if __name__ == '__main__':
    main() 
