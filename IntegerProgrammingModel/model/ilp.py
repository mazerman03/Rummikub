from ortools.linear_solver import pywraplp
from helper import JOKER_ID

status_map = {
    pywraplp.Solver.OPTIMAL: "OPTIMAL",
    pywraplp.Solver.FEASIBLE: "FEASIBLE",
    pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
    pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
    pywraplp.Solver.ABNORMAL: "ABNORMAL",
    pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
}



def solve_rummikub_ilp(sij, ti, ri, vi, wj=None, M=40):
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        raise RuntimeError("Failed to create solver instance.")

    I = list(ri.keys())
    J = list(set(j for (i, j) in sij))

    # Decision Variables
    xj = {j: solver.IntVar(0, 2, f'x_{j}') for j in J}  # Sets formed
    yi = {i: solver.IntVar(0, 2, f'y_{i}') for i in I}  # Tiles played

    # Secondary variables for minimizing changes
    zj = {j: solver.IntVar(0, 2, f'z_{j}') for j in J} if wj else {}

    # Objective Function
    objective = solver.Sum(vi[i] * yi[i] for i in I)
    if wj:
        objective += solver.Sum(zj[j] for j in J) / M
    solver.Maximize(objective)

    # Constraints
    for i in I:
        solver.Add(solver.Sum(sij.get((i, j), 0) * xj[j] for j in J) == ti.get(i, 0) + yi[i])

    for i in I:
        solver.Add(yi[i] <= ri[i])

    if wj:
        for j in J:
            solver.Add(zj[j] <= xj[j])
            solver.Add(zj[j] <= wj.get(j, 0))

    solver.Add(solver.Sum(sij.get((JOKER_ID, j), 0) * xj[j] for j in J) <= ri.get(JOKER_ID, 0))


    status = solver.Solve()
    status_str = status_map.get(status, "UNKNOWN")

    return {
        'status': status_str,
        'objective_value': solver.Objective().Value(),
        'played_tiles': {i: yi[i].solution_value() for i in I if yi[i].solution_value() > 0},
        'formed_sets': {j: xj[j].solution_value() for j in J if xj[j].solution_value() > 0},
        'kept_sets': {j: zj[j].solution_value() for j in J if wj and zj[j].solution_value() > 0} if wj else {}
    }
