from pysat.formula import CNF
from pysat.solvers import Glucose3

def var(i, j, d):
    """Map cell (i,j) with digit d to a unique variable."""
    return 100 * i + 10 * j + d

class SudokuSolver:
    def __init__(self):
        # Precompute universal CNF clauses that encode Sudoku rules.
        self.base_clauses = []
        
        # 1. Exactly one number per cell:
        for i in range(1, 10):
            for j in range(1, 10):
                clause = [var(i, j, d) for d in range(1, 10)]
                self.base_clauses.append(clause)
                # At most one number per cell (pairwise exclusion):
                for d1 in range(1, 10):
                    for d2 in range(d1 + 1, 10):
                        self.base_clauses.append([-var(i, j, d1), -var(i, j, d2)])
                        
        # 2. No repeat numbers in any row:
        for i in range(1, 10):
            for d in range(1, 10):
                for j1 in range(1, 10):
                    for j2 in range(j1 + 1, 10):
                        self.base_clauses.append([-var(i, j1, d), -var(i, j2, d)])
                        
        # 3. No repeat numbers in any column:
        for j in range(1, 10):
            for d in range(1, 10):
                for i1 in range(1, 10):
                    for i2 in range(i1 + 1, 10):
                        self.base_clauses.append([-var(i1, j, d), -var(i2, j, d)])
                        
        # 4. No repeat numbers in any 3x3 block:
        for blockRow in range(0, 3):
            for blockCol in range(0, 3):
                for d in range(1, 10):
                    cells = [(i, j)
                             for i in range(1 + blockRow * 3, 1 + blockRow * 3 + 3)
                             for j in range(1 + blockCol * 3, 1 + blockCol * 3 + 3)]
                    for idx in range(len(cells)):
                        for jdx in range(idx + 1, len(cells)):
                            i1, j1 = cells[idx]
                            i2, j2 = cells[jdx]
                            self.base_clauses.append([-var(i1, j1, d), -var(i2, j2, d)])

    def solve(self, board):
        """
        Solve a given 9x9 Sudoku board, where empty cells are 0.
        Returns a tuple (solved, solution) where solved is True if a solution exists.
        """
        cnf = CNF()
        # Load the universal constraints.
        for clause in self.base_clauses:
            cnf.append(clause)
            
        # Add board-specific constraints (fixed cells).
        for i in range(1, 10):
            for j in range(1, 10):
                d = int(board[i - 1][j - 1])
                if d != 0:
                    cnf.append([var(i, j, d)])
                    
        # Solve the CNF using Glucose3.
        with Glucose3(bootstrap_with=cnf) as solver:
            if solver.solve():
                model = solver.get_model()
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

if __name__ == '__main__':
    example_board = [
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [1, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 5, 0],
        [8, 0, 0, 0, 5, 0, 0, 0, 3]
    ]
    
    solver = SudokuSolver()  # Universal constraints computed once.
    solved, result_board = solver.solve(example_board)
    print("Solved:", solved)
    for row in result_board:
        print(row)
