import numpy as np
import random
from brute_force_solver import sudoku_brute_force

def generate_full_board():
    board = np.zeros((9, 9), dtype=int)
    solved, board = sudoku_brute_force(board)
    if solved:
        return board
    else:
        raise Exception("Failed to generate a full board.")

def remove_cells(board, removals):
    puzzle = board.copy()
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    count = 0
    for r, c in cells:
        if count >= removals:
            break
        puzzle[r, c] = 0
        count += 1
    return puzzle

def save_boards_to_txt(boards, filename):
    with open(filename, 'w') as f:
        for board in boards:
            for row in board:
                row_str = ' '.join(str(num) for num in row)
                f.write(row_str + '\n')
            f.write('\n')  

if __name__ == '__main__':
    num_puzzles = 1000 
    puzzles = []
    removals = 81
    for i in range(9*9): 
        removals -= 1
        if removals == 0:
            break 
        for i in range(num_puzzles):
            full_board = generate_full_board()
            puzzle = remove_cells(full_board, removals)
            puzzles.append(puzzle)
            
    

    save_boards_to_txt(puzzles, 'sudoku_puzzles.txt')
    print(f"{num_puzzles} Sudoku puzzles generated and saved to 'sudoku_puzzles.txt'")
