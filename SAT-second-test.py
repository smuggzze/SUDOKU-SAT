from pysat.solvers import Minisat22

with Minisat22(bootstrap_with=[[-1, 2], [-2, 3]]) as m:
     print(m.solve(assumptions=[1, -3]))
     print(m.get_core())
