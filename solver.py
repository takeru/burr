import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    from data import load_bars, Bar, bars_to_data
    from threejs import ThreeWidget
    import marimo as mo
    import numpy as np
    from blue import blue_puzzle_txt


@app.function
def has_common(aaa, bbb):
    for a in aaa:
        for b in bbb:
            if np.all(a == b):
                return True
    return False


@app.function
def has_common_fast(aaa, bbb):
    """高速化版: セットを使った衝突検出"""
    if len(aaa) == 0 or len(bbb) == 0:
        return False
    # 3D座標をタプルに変換してセット化
    aaa_set = {tuple(a) for a in aaa}
    bbb_set = {tuple(b) for b in bbb}
    # セットの積集合で衝突検出
    return len(aaa_set & bbb_set) > 0


@app.function
def has_common_fast_numpy(aaa, bbb):
    """高速化版: NumPyのブロードキャスティングを使った衝突検出"""
    if len(aaa) == 0 or len(bbb) == 0:
        return False
    # ブロードキャスティングで全ペアを一度に比較
    # aaa: (n, 3), bbb: (m, 3) -> (n, 1, 3) と (1, m, 3) で比較
    matches = (aaa[:, np.newaxis, :] == bbb[np.newaxis, :, :]).all(axis=2)
    return matches.any()


@app.function
def bars_to_voxels(bars):
    if len(bars) == 0:
        return np.empty((0, 3))
    voxels_list = []
    for bar in bars:
        voxels_list.append(bar.voxels())
    return np.concat(voxels_list)


@app.function
def solve(
    ctx, bars, placed_bar_and_patterns, bar_indices_to_placement, patterns
):
    # print(f"solve {placed_bar_and_patterns} {bar_indices_to_placement}")
    solutions = []
    bars_temp = []
    for placement, (bar_index, pattern) in enumerate(placed_bar_and_patterns):
        bar = bars[bar_index]
        bar.set_placement(placement)
        bar.set_pattern(pattern)
        bars_temp.append(bar)
    placed_voxcels = bars_to_voxels(bars_temp)

    for bar_index in bar_indices_to_placement:
        # print(f"bar_index={bar_index}")
        new_bar_indices_to_placement = [
            bi for bi in bar_indices_to_placement if bi != bar_index
        ]
        for pattern in patterns:
            new_bar = bars[bar_index]
            new_bar.set_placement(len(placed_bar_and_patterns))
            new_bar.set_pattern(pattern)
            new_bar_voxels = new_bar.voxels()
            has_collision = has_common_fast_numpy(
                placed_voxcels, new_bar_voxels
            )
            new_placed_bar_and_patterns = placed_bar_and_patterns + [
                (bar_index, pattern)
            ]
            if has_collision:
                pass
            else:
                if len(new_bar_indices_to_placement) == 0:
                    solution = new_placed_bar_and_patterns
                    ctx["callback"]({"solution": solution})
                    solutions.append(solution)
                else:
                    solutions += solve(
                        ctx,
                        bars,
                        new_placed_bar_and_patterns,
                        new_bar_indices_to_placement,
                        patterns,
                    )
    return solutions


@app.class_definition
class Solver:
    def __init__(self, txt):
        self.txt = txt
        self.reset()

    def reset(self):
        self.bars = load_bars(self.txt)

    def solve(self, callback, patterns=range(8)):
        self.reset()
        ctx = {"callback": callback}
        return solve(ctx, self.bars, [], [0, 1, 2, 3, 4, 5], patterns)
        # return solve(ctx, self.bars, [(5, 6)], [0, 1, 2, 3, 4], patterns)

    def solution_to_bars(self, s):
        _bars = []
        for placement, (bar_index, pattern) in enumerate(s):
            bar = self.bars[bar_index]
            bar.set_pattern(pattern)
            bar.set_placement(placement)
            _bars.append(bar)
        return _bars


@app.cell
def _(profile):
    solver = Solver(blue_puzzle_txt())


    def callback(x):
        print(x)


    # patterns=[0, 6]
    with profile(False):
        solutions = solver.solve(callback)

    print("done")
    return callback, solutions, solver


@app.cell
def _(callback, solver):
    solver.solve(callback)
    return


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
def _(slider, solution):
    [slider, str(solution)]
    return


@app.cell
def _(solutions):
    slider = mo.ui.slider(start=0, stop=len(solutions) - 1)
    return (slider,)


@app.cell
def _(slider, solutions, solver, widget):
    solution = solutions[slider.value]
    _bars = solver.solution_to_bars(solution)
    widget.data = bars_to_data(_bars)
    return (solution,)


@app.cell
def _():
    _a = np.array([[1, 2, 3]])
    _b = np.array([[4, 5, 6]])
    _c = np.array([[1, 2, 2]])
    _ab = np.array([[1, 2, 3], [4, 5, 6]])

    # 元の関数のテスト
    assert has_common(_a, _b) == False
    assert has_common(_a, _c) == False
    assert has_common(_a, _ab) == True
    assert has_common(_ab, _a) == True
    assert has_common(_b, _ab) == True
    assert has_common(_ab, _b) == True

    # has_common_fast (セット版) のテスト
    assert has_common_fast(_a, _b) == False
    assert has_common_fast(_a, _c) == False
    assert has_common_fast(_a, _ab) == True
    assert has_common_fast(_ab, _a) == True
    assert has_common_fast(_b, _ab) == True
    assert has_common_fast(_ab, _b) == True

    # has_common_fast_numpy (NumPy版) のテスト
    assert has_common_fast_numpy(_a, _b) == False
    assert has_common_fast_numpy(_a, _c) == False
    assert has_common_fast_numpy(_a, _ab) == True
    assert has_common_fast_numpy(_ab, _a) == True
    assert has_common_fast_numpy(_b, _ab) == True
    assert has_common_fast_numpy(_ab, _b) == True

    print("全てのhas_common関数のテストが成功しました！")
    return


@app.cell
def _():
    import cProfile
    import pstats
    from io import StringIO
    import time

    from contextlib import contextmanager


    @contextmanager
    def profile(enable):
        profiler = None
        if enable:
            profiler = cProfile.Profile()
            profiler.enable()

        start_time = time.time()
        yield
        end_time = time.time()

        print(f"{end_time - start_time:.3f} seconds.")
        if enable:
            profiler.disable()

            s = StringIO()
            ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
            ps.print_stats(20)

            print(s.getvalue())
    return (profile,)


if __name__ == "__main__":
    app.run()
