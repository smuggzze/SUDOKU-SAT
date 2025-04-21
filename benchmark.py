import numpy as np
import time
import pandas as pd
from tqdm import tqdm
from brute_force_solver import sudoku_brute_force 
from sat_solver import SudokuSolver 

def load_boards_from_txt(filename):
    # (Keep the same implementation as before)
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

def print_summary(results):
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
    results = []  # List to store benchmarking results.
    
    # Initialize the SAT solver once.
    sat_solver = SudokuSolver()
    
    # Process each board with a progress bar.
    for i, board in enumerate(tqdm(boards, desc="Processing boards"), start=1):
        # Record the number of removals (i.e. zeros in the board)
        removals = int(np.sum(board == 0))
        
        # --- Brute Force Solver Benchmark ---
        bf_start = time.time() * 1000  # ms
        solved_brute, solved_board = sudoku_brute_force(board.copy())
        bf_end = time.time() * 1000
        brute_time = bf_end - bf_start
        results.append({
            'board_index': i,
            'solver': 'brute',
            'time_ms': brute_time,
            'removals': removals,
            'outcome': 'solved' if solved_brute else 'DNF'
        })
        
        # --- SAT Solver Benchmark ---
        sat_start = time.time() * 1000  # ms
        solved_sat, solved_board = sat_solver.solve(board.copy())
        sat_end = time.time() * 1000
        sat_time = sat_end - sat_start
        results.append({
            'board_index': i,
            'solver': 'sat',
            'time_ms': sat_time,
            'removals': removals,
            'outcome': 'solved' if solved_sat else 'DNF'
        })
    
    print_summary(results)
    
    # Save the results to CSV for plotting.
    df = pd.DataFrame(results)
    df.to_csv('benchmark_results.csv', index=False)
    print("Results saved to benchmark_results.csv")

if __name__ == '__main__':
    main()
