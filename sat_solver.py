from pysat.formula import CNF
from pysat.solvers import Glucose3

def var(i, j, d):
    """Map cell (i,j) with digit d to a unique variable."""
    return 100 * i + 10 * j + d

def sudoku_sat(board):
    """
    Given a 9x9 board (list of lists or NumPy array), where 0 indicates an empty cell,
    returns a tuple (solved, solution) where solved is True if a solution exists.
    """
    cnf = CNF()

    # 1. Exactly one number per cell
    for i in range(1, 10):
        for j in range(1, 10):
            clause = [var(i, j, d) for d in range(1, 10)]
            cnf.append(clause)
            # At most one number: pairwise exclusion
            for d1 in range(1, 10):
                for d2 in range(d1 + 1, 10):
                    cnf.append([-var(i, j, d1), -var(i, j, d2)])

    # 2. No repeat numbers in any row
    for i in range(1, 10):
        for d in range(1, 10):
            for j1 in range(1, 10):
                for j2 in range(j1 + 1, 10):
                    cnf.append([-var(i, j1, d), -var(i, j2, d)])
                    
    # 3. No repeat numbers in any column
    for j in range(1, 10):
        for d in range(1, 10):
            for i1 in range(1, 10):
                for i2 in range(i1 + 1, 10):
                    cnf.append([-var(i1, j, d), -var(i2, j, d)])
    
    # 4. No repeat numbers in any 3x3 block
    for blockRow in range(0, 3):
        for blockCol in range(0, 3):
            for d in range(1, 10):
                # Get the cells in this block:
                cells = [(i, j)
                         for i in range(1 + blockRow * 3, 1 + blockRow * 3 + 3)
                         for j in range(1 + blockCol * 3, 1 + blockCol * 3 + 3)]
                for idx in range(len(cells)):
                    for jdx in range(idx + 1, len(cells)):
                        i1, j1 = cells[idx]
                        i2, j2 = cells[jdx]
                        cnf.append([-var(i1, j1, d), -var(i2, j2, d)])
                        
    # 5. Fixed cells: add unit clauses for pre-filled cells.
    for i in range(1, 10):
        for j in range(1, 10):
            # Cast the value to int in case it's a numpy.int64
            d = int(board[i - 1][j - 1])
            if d != 0:
                cnf.append([var(i, j, d)])
                
    # Solve the CNF formula using Glucose3.
    with Glucose3(bootstrap_with=cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            if model is None:
                return False, board  # Defensive check
            # Build the solution board.
            solution = [[0 for _ in range(9)] for _ in range(9)]
            for v in model:
                if v > 0:
                    d = v % 10
                    j = (v // 10) % 10
                    i = v // 100
                    solution[i - 1][j - 1] = d
            return True, solution
        else:
            return False, board

# Example usage (for testing purposes only):
if __name__ == '__main__':
    example_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    solved, result_board = sudoku_sat(example_board)
    print(solved)
    print(result_board)

# Example usage (for testing purposes only):
if __name__ == '__main__':
    example_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    solved, result_board = sudoku_sat(example_board)
    print(solved)
    print(result_board)
