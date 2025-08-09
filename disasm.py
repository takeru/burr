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


@app.cell
def _():
    solver = Solver(blue_puzzle_txt())
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
    return (bars,)


@app.function
def moved_bars(bars, bar_indices, xyz):
    for bar in bars:
        bar.position.x = 0
        bar.position.y = 0
        bar.position.z = 0
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


@app.cell
def _(bars):
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
                if can_move(bars, bar_indices, xyz):
                    moves.append({"bar_indices": bar_indices, "xyz": xyz})
                    print(f"found: bar_indices={bar_indices} xyz={xyz}")
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


if __name__ == "__main__":
    app.run()
