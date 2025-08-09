import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    from solver import Solver, bars_to_voxels
    import marimo as mo
    from blue import blue_puzzle_txt
    from threejs import ThreeWidget
    from data import bars_to_data
    from itertools import combinations
    import numpy as np
    from probrems import love_dozen, without_internal_voids, simple_notches


@app.cell
def _():
    solver = Solver(blue_puzzle_txt())
    # solver = Solver(love_dozen())
    # solver = Solver(without_internal_voids())
    # solver = Solver(simple_notches())
    return (solver,)


@app.cell
def _(solver):
    def callback(x):
        print(x)


    solutions = solver.solve(callback)
    print("done")
    return (solutions,)


@app.cell
def _(solver):
    solver.bars
    return


@app.cell
def _(solutions):
    solution_index = mo.ui.slider(start=0, stop=len(solutions) - 1)
    return (solution_index,)


@app.cell
def _(solution_index, solutions, solver):
    solution = solutions[solution_index.value]
    bars = solver.solution_to_bars(solution)
    return bars, solution


@app.function
def moved_bars(bars, bar_indices, xyz):
    for bi in bar_indices:
        bar = bars[bi]
        bar.position.x = xyz[0]
        bar.position.y = xyz[1]
        bar.position.z = xyz[2]
    return bars


@app.function
def can_move(bars, bar_indices, xyz):
    bars = moved_bars(bars, bar_indices, xyz)
    voxels = np.array(bars_to_voxels(bars))
    is_unique = len(np.unique(voxels, axis=0)) == len(voxels)
    return is_unique


@app.function
def find_moves(bars, state):
    moves = []
    for bar_count in [1, 2, 3]:
        bar_indices_combs = list(combinations(range(6), bar_count))
        for bar_indices in bar_indices_combs:
            for xyz in [
                [1, 0, 0],
                [-1, 0, 0],
                [0, 1, 0],
                [0, -1, 0],
                [0, 0, 1],
                [0, 0, -1],
            ]:
                for b, p in zip(bars, state.positions):
                    b.position.x = p[0]
                    b.position.y = p[1]
                    b.position.z = p[2]
                if can_move(bars, bar_indices, xyz):
                    moves.append({"bar_indices": bar_indices, "xyz": xyz})
                    # print(f"found: bar_indices={bar_indices} xyz={xyz}")
    return moves


@app.cell
def _(bars):
    moves = find_moves(bars, BarPositionsState())
    return (moves,)


@app.cell
def _():
    widget = ThreeWidget()
    widget.data = []
    return (widget,)


@app.cell
def _(widget):
    widget
    return


@app.cell
def _(moves):
    move_index = mo.ui.slider(start=0, stop=len(moves) - 1)
    return (move_index,)


@app.cell
def _():
    move_progress = mo.ui.slider(start=0, stop=10, value=1, step=0.1)
    return (move_progress,)


@app.cell
def _(move_index, move_progress, solution_index):
    mo.md(
        f"""
    - {solution_index}
    - {move_index}
    - {move_progress}
    """
    )
    return


@app.cell
def _(bars, move_index, move_progress, moves, widget):
    move = moves[move_index.value]
    _bars = moved_bars(
        bars, move["bar_indices"], np.array(move["xyz"]) * move_progress.value
    )
    widget.data = bars_to_data(_bars)
    return


@app.class_definition
class BarPositionsState:
    def __init__(self):
        self.parent = None
        self.positions = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.next_states = None

    def positions_flat(self):
        flat = []
        for p in self.positions:
            flat += p
        return flat


@app.cell
def _(bars):
    def find_next_states(state, known_keys):
        moves = find_moves(bars, state)
        next_states = []
        for m in moves:
            bi = m["bar_indices"]
            xyz = m["xyz"]
            s = BarPositionsState()
            s.parent = state
            for i, p in enumerate(s.positions):
                p[0] = state.positions[i][0]
                p[1] = state.positions[i][1]
                p[2] = state.positions[i][2]
                # print(f"{xyz=} {i=} {p=}")
                if i in bi:
                    p[0] += xyz[0]
                    p[1] += xyz[1]
                    p[2] += xyz[2]

            key = ",".join([str(v) for v in s.positions_flat()])
            if key in known_keys:
                pass
            else:
                # print(s.positions)
                known_keys.add(key)
                # if any([v <= -7 or 7 <= v for v in s.positions_flat()]):
                #     print(s.positions)
                #     pass
                # else:
                #     s.next_states = find_next_states(s, known_keys)
                next_states.append(s)
        return next_states
    return (find_next_states,)


@app.cell
def _(find_next_states):
    class DisassembleStepSolver:
        def __init__(self, assembled):
            self.assembled = assembled
            self.root = BarPositionsState()

        def solve(self):
            known_keys = set()
            states = [self.root]
            depth = 0
            while True:
                print(f"depth={depth} len(states)={len(states)}")
                new_states = []
                for s in states:
                    ss = find_next_states(s, known_keys)
                    s.next_states = ss
                    new_states += ss
                states = new_states
                depth += 1
    return (DisassembleStepSolver,)


@app.cell
def _(solution_index):
    solution_index
    return


@app.cell
def _(DisassembleStepSolver, solution):
    dsolver = DisassembleStepSolver(solution)
    dsolver.solve()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
