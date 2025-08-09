import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    import cProfile
    import pstats
    from io import StringIO
    import time
    from data import load_bars, Bar, bars_to_data
    from blue import blue_puzzle_txt
    import numpy as np
    import marimo as mo
    # solver.pyから関数をインポート
    from solver import (
        has_common, has_common_fast, has_common_fast_numpy,
        solve, bars_to_voxels, Solver
    )


@app.cell
def _():
    mo.md("# Solver プロファイリング")
    return


@app.cell
def _():
    def profile_solve_function():
        """solve関数のプロファイリング"""
        solver = Solver(blue_puzzle_txt())
        
        def callback(x):
            pass  # プロファイリング時は出力を抑制
        
        # プロファイリング開始
        profiler = cProfile.Profile()
        profiler.enable()
        
        start_time = time.time()
        solutions = solver.solve(callback, patterns=[0, 6])  # 少ないパターンでテスト
        end_time = time.time()
        
        profiler.disable()
        
        # 結果を文字列として取得
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(20)
        
        result = f"実行時間: {end_time - start_time:.3f}秒\n"
        result += f"解の数: {len(solutions)}\n\n"
        result += "=== プロファイリング結果 (累積時間順) ===\n"
        result += s.getvalue()
        
        return result, solutions
    
    return profile_solve_function,


@app.cell
def _(profile_solve_function):
    profile_result, solutions = profile_solve_function()
    return profile_result, solutions


@app.cell
def _(mo, profile_result):
    mo.md(f"```\n{profile_result}\n```")
    return


@app.cell
def _():
    mo.md("## has_common 関数の性能比較")
    return


@app.cell
def _():
    def compare_has_common():
        """has_common関数の性能比較"""
        import timeit
        
        # テストデータの準備
        np.random.seed(42)
        small_array = np.random.randint(0, 10, (10, 3))
        large_array = np.random.randint(0, 10, (100, 3))
        test_array = np.random.randint(0, 10, (20, 3))
        
        iterations = 1000
        
        results = []
        
        # 小さい配列でのテスト
        results.append("=== 小さい配列 (10 x 3) ===")
        
        time_original = timeit.timeit(
            lambda: has_common(small_array, test_array),
            number=iterations
        )
        results.append(f"has_common (オリジナル): {time_original:.4f}秒")
        
        time_fast = timeit.timeit(
            lambda: has_common_fast(small_array, test_array),
            number=iterations
        )
        results.append(f"has_common_fast (セット版): {time_fast:.4f}秒")
        results.append(f"速度向上: {time_original/time_fast:.2f}倍")
        
        time_numpy = timeit.timeit(
            lambda: has_common_fast_numpy(small_array, test_array),
            number=iterations
        )
        results.append(f"has_common_fast_numpy (NumPy版): {time_numpy:.4f}秒")
        results.append(f"速度向上: {time_original/time_numpy:.2f}倍")
        
        # 大きい配列でのテスト
        results.append("\n=== 大きい配列 (100 x 3) ===")
        
        iterations_large = 100
        
        time_original = timeit.timeit(
            lambda: has_common(large_array, test_array),
            number=iterations_large
        )
        results.append(f"has_common (オリジナル): {time_original:.4f}秒")
        
        time_fast = timeit.timeit(
            lambda: has_common_fast(large_array, test_array),
            number=iterations_large
        )
        results.append(f"has_common_fast (セット版): {time_fast:.4f}秒")
        results.append(f"速度向上: {time_original/time_fast:.2f}倍")
        
        time_numpy = timeit.timeit(
            lambda: has_common_fast_numpy(large_array, test_array),
            number=iterations_large
        )
        results.append(f"has_common_fast_numpy (NumPy版): {time_numpy:.4f}秒")
        results.append(f"速度向上: {time_original/time_numpy:.2f}倍")
        
        return "\n".join(results)
    
    return compare_has_common,


@app.cell
def _(compare_has_common):
    comparison_result = compare_has_common()
    return comparison_result,


@app.cell
def _(comparison_result, mo):
    mo.md(f"```\n{comparison_result}\n```")
    return


@app.cell
def _():
    mo.md("## 詳細なプロファイリング結果の分析")
    return


@app.cell
def _():
    def analyze_profiling():
        """プロファイリング結果の詳細分析"""
        solver = Solver(blue_puzzle_txt())
        
        # 少量のデータでプロファイリング
        profiler = cProfile.Profile()
        profiler.enable()
        
        def callback(x):
            pass
        
        solutions = solver.solve(callback, patterns=[0])  # 1パターンのみ
        
        profiler.disable()
        
        # 統計情報を取得
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        # 関数ごとの統計を取得
        func_stats = []
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            filename, line, func_name = func
            if 'solver' in filename or 'data' in filename:
                func_stats.append({
                    'function': f"{func_name} ({filename}:{line})",
                    'calls': nc,
                    'total_time': tt,
                    'cumulative_time': ct,
                    'per_call': tt/nc if nc > 0 else 0
                })
        
        # 上位10個の関数を表示
        func_stats.sort(key=lambda x: x['cumulative_time'], reverse=True)
        
        result = "=== 最も時間がかかっている関数 (solver.py, data.py) ===\n"
        for stat in func_stats[:10]:
            result += f"\n{stat['function']}\n"
            result += f"  呼び出し回数: {stat['calls']}\n"
            result += f"  総時間: {stat['total_time']:.6f}秒\n"
            result += f"  累積時間: {stat['cumulative_time']:.6f}秒\n"
            result += f"  平均時間/呼び出し: {stat['per_call']:.6f}秒\n"
        
        return result
    
    return analyze_profiling,


@app.cell
def _(analyze_profiling):
    detailed_analysis = analyze_profiling()
    return detailed_analysis,


@app.cell
def _(detailed_analysis, mo):
    mo.md(f"```\n{detailed_analysis}\n```")
    return


if __name__ == "__main__":
    app.run()