#!/usr/bin/env python
"""solver.pyのプロファイリング用スクリプト"""

import cProfile
import pstats
from io import StringIO
import time

# 必要なモジュールをインポート
from data import load_bars, bars_to_data
from blue import blue_puzzle_txt
import numpy as np

# solver.pyから関数を直接インポート
exec(open('solver.py').read())

def profile_solve():
    """solve関数のプロファイリング"""
    solver = Solver(blue_puzzle_txt())
    
    def callback(x):
        pass  # プロファイリング時は出力を抑制
    
    # プロファイリング開始
    start_time = time.time()
    solutions = solver.solve(callback, patterns=range(8))
    end_time = time.time()
    
    print(f"\n実行時間: {end_time - start_time:.3f}秒")
    print(f"解の数: {len(solutions)}")
    
    return solutions

def compare_has_common_functions():
    """has_common関数の性能比較"""
    import timeit
    
    # テストデータの準備
    np.random.seed(42)
    small_array = np.random.randint(0, 10, (10, 3))
    large_array = np.random.randint(0, 10, (100, 3))
    test_array = np.random.randint(0, 10, (20, 3))
    
    # 各関数の実行時間を測定
    iterations = 1000
    
    print("\n=== has_common関数の性能比較 ===")
    print(f"テスト回数: {iterations}回")
    
    # 小さい配列でのテスト
    print("\n小さい配列 (10 x 3):")
    
    time_original = timeit.timeit(
        lambda: has_common(small_array, test_array),
        number=iterations
    )
    print(f"  has_common (オリジナル): {time_original:.4f}秒")
    
    time_fast = timeit.timeit(
        lambda: has_common_fast(small_array, test_array),
        number=iterations
    )
    print(f"  has_common_fast (セット版): {time_fast:.4f}秒")
    print(f"  速度向上: {time_original/time_fast:.2f}倍")
    
    time_numpy = timeit.timeit(
        lambda: has_common_fast_numpy(small_array, test_array),
        number=iterations
    )
    print(f"  has_common_fast_numpy (NumPy版): {time_numpy:.4f}秒")
    print(f"  速度向上: {time_original/time_numpy:.2f}倍")
    
    # 大きい配列でのテスト
    print("\n大きい配列 (100 x 3):")
    
    time_original = timeit.timeit(
        lambda: has_common(large_array, test_array),
        number=iterations//10
    )
    print(f"  has_common (オリジナル): {time_original:.4f}秒")
    
    time_fast = timeit.timeit(
        lambda: has_common_fast(large_array, test_array),
        number=iterations//10
    )
    print(f"  has_common_fast (セット版): {time_fast:.4f}秒")
    print(f"  速度向上: {time_original/time_fast:.2f}倍")
    
    time_numpy = timeit.timeit(
        lambda: has_common_fast_numpy(large_array, test_array),
        number=iterations//10
    )
    print(f"  has_common_fast_numpy (NumPy版): {time_numpy:.4f}秒")
    print(f"  速度向上: {time_original/time_numpy:.2f}倍")

if __name__ == "__main__":
    print("=== Solver全体のプロファイリング ===")
    
    # cProfileでプロファイリング
    profiler = cProfile.Profile()
    profiler.enable()
    
    solutions = profile_solve()
    
    profiler.disable()
    
    # 結果を表示
    print("\n=== プロファイリング結果 (累積時間順) ===")
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(30)
    
    # solve関連の行だけ抽出
    output = s.getvalue()
    lines = output.split('\n')
    
    print("関数別の実行時間:")
    for line in lines:
        if any(keyword in line for keyword in ['solve', 'has_common', 'voxels', 'Bar', 'set_pattern', 'set_placement']):
            print(line)
    
    # has_common関数の比較
    compare_has_common_functions()