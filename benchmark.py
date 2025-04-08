import numpy as np
import time
import pandas as pd
from tqdm import tqdm
from brute_force_solver import sudoku_brute_force 
from sat_solver import SudokuSolver 

def load_boards_from_txt(filename):
    """
    Input: file consisting of sudoku grids (currently 9x9 only compatible)
    Converts file contents to numpy arrays as necessary.
    Returns: list of np.array boards.
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
    Input: np.array of sudoku
    Prints the board in a human-readable format.
    """
    if isinstance(board, np.ndarray):
        board = board.tolist()
    for row in board:
        print(" ".join(str(num) for num in row))

def print_summary(results):
    """
    Print summary statistics grouped by solver using the results list.
    """
    df = pd.DataFrame(results)
    grouped = df.groupby("solver").agg({
        "time_ms": ["mean", "min", "max", "std"],
        "board_index": "count"
    })
    print("Summary by Solver:")
    print(grouped)
    
def main():
    filename = 'sudoku_puzzles.txt'
    boards = load_boards_from_txt(filename)
    results = []  # List to store benchmarking results for each board & solver.
    
    # Initialize the SAT solver once.
    sat_solver = SudokuSolver()
    
    # Wrap the boards iterable with tqdm to display a progress bar.
    for i, board in enumerate(tqdm(boards, desc="Processing boards"), start=1):
        
        # --- Brute Force Solver Benchmark ---
        start_time = time.time() * 1000  # time in milliseconds
        solved_brute, solved_board = sudoku_brute_force(board.copy())
        end_time = time.time() * 1000
        brute_time = end_time - start_time

        results.append({
            'board_index': i,
            'solver': 'brute',
            'time_ms': brute_time if solved_brute else None,
            'outcome': 'solved' if solved_brute else 'DNF'
        })
        
        # --- SAT Solver Benchmark ---
        start_time = time.time() * 1000  # time in milliseconds
        solved_sat, solved_board = sat_solver.solve(board.copy())
        end_time = time.time() * 1000
        sat_time = end_time - start_time

        results.append({
            'board_index': i,
            'solver': 'sat',
            'time_ms': sat_time if solved_sat else None,
            'outcome': 'solved' if solved_sat else 'DNF'
        })
    
    # Print a summary of the benchmark results.
    print_summary(results)
    
    # Write full results to a CSV file.
    df = pd.DataFrame(results)
    csv_filename = 'benchmark_results.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Results saved to {csv_filename}")

if __name__ == '__main__':
    main()
