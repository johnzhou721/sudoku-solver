from pysat.formula import *
from pysat.solvers import Solver
import time

def get_id(row, col, val):
    return (row - 1) * 81 + (col - 1) * 9 + val

def gen_clauses():
    def exactly_one(values):
        clauses = []

        # ensure at least 1 true
        clauses.append([v for v in values])

        # ensure no two clauses are both on
        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                clauses.append([-values[i], -values[j]])
        return clauses
    
    clauses = []
    
    # ensure each cell only has one value
    for row in range(1, 10):
        for col in range(1, 10):
            ids = [get_id(row, col, val) for val in range(1, 10)]
            clauses += exactly_one(ids)

    # ensure each row has one of each value
    for row in range(1, 10):
        for val in range(1, 10):
            ids = [get_id(row, col, val) for col in range(1, 10)]
            clauses += exactly_one(ids)

    # ensure each col has one of each value
    for col in range(1, 10):
        for val in range(1, 10):
            ids = [get_id(row, col, val) for row in range(1, 10)]
            clauses += exactly_one(ids)

    # ensure each subgrid has one of each value
    for row in range(1, 10, 3):
        for col in range(1, 10, 3):
            # subgrid starts at (row, col)
            for val in range(1, 10):
                ids = [get_id(row + x, col + y, val) for x in range(0, 3) for y in range(0, 3)]
                clauses += exactly_one(ids)

    return clauses

UNSATISFIABLE = object()

def solve(clues):
    clauses = gen_clauses()

    # clues are the already-filled cells
    for r, c, v in clues:
        clauses.append([get_id(r, c, v)])  # unit clause for a clue

    cnf = CNF(from_clauses=clauses)

    with Solver(bootstrap_with=cnf.clauses) as s:
        sat = s.solve()
        if not sat:
            return UNSATISFIABLE
        else:
            model = s.get_model()

            # extract positive literals that correspond to (r,c,v)
            grid = [[0] * 9 for _ in range(9)]
            for lit in model:
                if lit > 0 and 1 <= lit <= 729:
                    idx = lit - 1
                    row = idx // 81 + 1
                    col = (idx % 81) // 9 + 1
                    val = idx % 9 + 1
                    grid[row - 1][col - 1] = val

    return grid

__all__ = ["solve", "UNSATISFIABLE"]