import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    from threejs import ThreeWidget
    from typing import List
    from dataclasses import dataclass
    import numpy as np
    from functools import cache


@app.class_definition
@dataclass
class Rotation:
    x: int
    y: int
    z: int


@app.class_definition
@dataclass
class Position:
    x: int
    y: int
    z: int


@app.cell(hide_code=True)
def _():
    mo.md(r"""# Local Rotation / Global Rotation""")
    return


@app.cell
def _():
    widget01 = ThreeWidget()
    widget01.data = []

    rotation_sliders = mo.ui.dictionary(
        elements={
            "local_rotation_x": mo.ui.slider(start=0, stop=3),
            "local_rotation_y": mo.ui.slider(start=0, stop=3),
            "local_rotation_z": mo.ui.slider(start=0, stop=3),
            "global_rotation_x": mo.ui.slider(start=0, stop=3),
            "global_rotation_y": mo.ui.slider(start=0, stop=3),
            "global_rotation_z": mo.ui.slider(start=0, stop=3),
        }
    )
    return rotation_sliders, widget01


@app.cell
def _(rotation_sliders, widget01):
    b0 = Bar(
        np.array(
            [
                [True, False, False, False],
                [False, False, False, False],
                [True, True, True, True],
                [True, True, True, True],
            ]
        )
    )
    b0.local_rotation.x = rotation_sliders["local_rotation_x"].value
    b0.local_rotation.y = rotation_sliders["local_rotation_y"].value
    b0.local_rotation.z = rotation_sliders["local_rotation_z"].value
    b0.global_rotation.x = rotation_sliders["global_rotation_x"].value
    b0.global_rotation.y = rotation_sliders["global_rotation_y"].value
    b0.global_rotation.z = rotation_sliders["global_rotation_z"].value
    b0.color = "#00aa00"

    _bars = []
    _bars.append(b0)
    widget01.data = bars_to_data(_bars)
    return


@app.cell
def _(widget01):
    widget01
    return


@app.cell
def _(rotation_sliders):
    rotation_sliders
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""# Pattern(Local Roration) + Offset(Position)""")
    return


@app.cell
def _():
    pat = mo.ui.slider(start=0, stop=7)
    ofs = mo.ui.slider(start=0, stop=10, step=0.2)

    _bar_txt = """
    1000
    1000
    1111
    1111
    ----
    """
    debug_txt = f"""
    ----
    {_bar_txt * 6}
    """.strip()
    bars02 = load_bars(debug_txt)
    widget02 = ThreeWidget()
    widget02.data = []
    return bars02, ofs, pat, widget02


@app.cell
def _(widget02):
    widget02
    return


@app.cell
def _(ofs, pat):
    mo.md(
        f"""
    - pat: {pat} {pat.value}
    - ofs: {ofs} {ofs.value}
    """
    )
    return


@app.cell
def _(bars02, ofs, pat, widget02):
    for i, bar in enumerate(bars02):
        if i == 1 or i == 3:
            bar.position.x = ofs.value
        if i == 2 or i == 4:
            bar.position.z = ofs.value

        bar.set_pattern(pat.value)

    widget02.data = bars_to_data(bars02)
    return


@app.function
def bits_to_voxels(
    bits: np.ndarray,
    local_rotation: Rotation,
    global_rotation: Rotation,
    position: Position,
):
    # bits: np.ndarray
    assert bits.shape == (4, 4)
    voxels = []
    for i, bbbb in enumerate(bits):
        y = -1 - (i // 2)
        z = i % 2 - 1
        for x, b in enumerate(bbbb):
            if b:
                voxels.append([x - 2, y, z])
    for x in [-3, 2]:
        for y in [-2, -1]:
            for z in [-1, 0]:
                voxels.append([x, y, z])

    # 90度単位の sin/cos 値の事前定義（整数値）
    # cos(0°)=1, cos(90°)=0, cos(180°)=-1, cos(270°)=0
    # sin(0°)=0, sin(90°)=1, sin(180°)=0, sin(270°)=-1
    cos_values = [1, 0, -1, 0]
    sin_values = [0, 1, 0, -1]

    # ローカル回転の中心点
    local_center = [-0.5, -1.5, -0.5]

    # 1. ローカル回転を適用
    # 回転角度を0-3の範囲に正規化
    lrx = local_rotation.x % 4
    lry = local_rotation.y % 4
    lrz = local_rotation.z % 4

    # ローカル回転行列を作成（事前定義された値を使用）
    # X軸回転
    LRx = np.array(
        [
            [1, 0, 0],
            [0, cos_values[lrx], -sin_values[lrx]],
            [0, sin_values[lrx], cos_values[lrx]],
        ]
    )

    # Y軸回転
    LRy = np.array(
        [
            [cos_values[lry], 0, sin_values[lry]],
            [0, 1, 0],
            [-sin_values[lry], 0, cos_values[lry]],
        ]
    )

    # Z軸回転
    LRz = np.array(
        [
            [cos_values[lrz], -sin_values[lrz], 0],
            [sin_values[lrz], cos_values[lrz], 0],
            [0, 0, 1],
        ]
    )

    # 合成ローカル回転行列
    LR = LRz @ LRy @ LRx

    # ローカル回転を適用
    local_rotated_voxels = []
    for v in voxels:
        # 中心点を原点に移動
        translated = np.array(
            [
                v[0] - local_center[0],
                v[1] - local_center[1],
                v[2] - local_center[2],
            ]
        )

        # ローカル回転を適用
        rotated = LR @ translated

        # 中心点を元に戻す
        final = [
            rotated[0] + local_center[0],
            rotated[1] + local_center[1],
            rotated[2] + local_center[2],
        ]
        local_rotated_voxels.append(final)

    # 2. グローバル回転を適用
    # グローバル回転の中心点
    global_center = [-0.5, -0.5, -0.5]

    # 回転角度を0-3の範囲に正規化
    grx = global_rotation.x % 4
    gry = global_rotation.y % 4
    grz = global_rotation.z % 4

    # グローバル回転行列を作成（事前定義された値を使用）

    # X軸回転
    GRx = np.array(
        [
            [1, 0, 0],
            [0, cos_values[grx], -sin_values[grx]],
            [0, sin_values[grx], cos_values[grx]],
        ]
    )

    # Y軸回転
    GRy = np.array(
        [
            [cos_values[gry], 0, sin_values[gry]],
            [0, 1, 0],
            [-sin_values[gry], 0, cos_values[gry]],
        ]
    )

    # Z軸回転
    GRz = np.array(
        [
            [cos_values[grz], -sin_values[grz], 0],
            [sin_values[grz], cos_values[grz], 0],
            [0, 0, 1],
        ]
    )

    # 合成グローバル回転行列
    # GR = GRz @ GRy @ GRx
    GR = GRx @ GRy @ GRz

    # グローバル回転を適用
    global_rotated_voxels = []
    for v in local_rotated_voxels:
        # 中心点を原点に移動
        translated = np.array(
            [
                v[0] - global_center[0],
                v[1] - global_center[1],
                v[2] - global_center[2],
            ]
        )

        # グローバル回転を適用
        rotated = GR @ translated

        # 中心点を元に戻して、最も近い整数座標に丸める
        final = np.round(
            [
                rotated[0] + global_center[0],
                rotated[1] + global_center[1],
                rotated[2] + global_center[2],
            ]
        ).astype(int)

        global_rotated_voxels.append(final.tolist())

    # 3. 位置を適用
    final_voxels = []
    for v in global_rotated_voxels:
        final_voxels.append(
            [v[0] + position.x, v[1] + position.y, v[2] + position.z]
        )

    return np.array(final_voxels)


@app.function
@cache
def bits_to_voxels_cached_tuple(
    bits_tuple: tuple,  # bitsをタプル化（4x4のブール値のタプル）
    local_rotation_tuple: tuple,
    global_rotation_tuple: tuple,
    position_tuple: tuple,
):
    """キャッシュ可能なbits_to_voxels関数"""
    # タプルをnumpy配列に戻す
    bits = np.array(bits_tuple, dtype=bool).reshape(4, 4)

    # Rotationオブジェクトを作成
    local_rotation = Rotation(
        local_rotation_tuple[0],
        local_rotation_tuple[1],
        local_rotation_tuple[2],
    )
    global_rotation = Rotation(
        global_rotation_tuple[0],
        global_rotation_tuple[1],
        global_rotation_tuple[2],
    )
    position = Position(
        position_tuple[0], position_tuple[1], position_tuple[2]
    )

    # 既存のbits_to_voxels関数を呼び出す
    result = bits_to_voxels(bits, local_rotation, global_rotation, position)

    # 結果をタプルとして返す（キャッシュの効率化のため）
    return tuple(map(tuple, result))


@app.function
def bits_to_voxels_cached(
    bits: np.ndarray,
    local_rotation: Rotation,
    global_rotation: Rotation,
    position: Position,
):
    # bitsをタプル化
    bits_tuple = tuple(tuple(row) for row in bits)

    # キャッシュ版の関数を呼び出す
    result_tuples = bits_to_voxels_cached_tuple(
        bits_tuple,
        tuple([local_rotation.x, local_rotation.y, local_rotation.z]),
        tuple([global_rotation.x, global_rotation.y, global_rotation.z]),
        tuple([position.x, position.y, position.z]),
    )

    # タプルをnumpy配列に戻す
    return np.array(result_tuples)


@app.cell
def _(ofs, pat):
    mo.md(
        f"""
    - pat: {pat} {pat.value}
    - ofs: {ofs} {ofs.value}
    """
    )
    return


@app.function
def global_rotation_for_placement(placement: int):
    a = [0, 0, 0]
    f = [0, 0, 2]
    b = [0, 1, 3]
    d = [0, 1, 1]
    c = [1, 0, 3]
    e = [1, 0, 1]
    return [a, b, c, d, e, f][placement]


@app.cell
def _(widget02):
    widget02
    return


@app.class_definition
class Bar:
    def __init__(self, bits: np.ndarray):
        assert bits.shape == (4, 4) and bits.dtype == bool
        self._bits = bits
        self.local_rotation = Rotation(0, 0, 0)
        self.global_rotation = Rotation(0, 0, 0)
        self.position = Position(0, 0, 0)
        self.color = "gray"

    def voxels(self):
        return bits_to_voxels_cached(
            # return bits_to_voxels(
            self._bits,
            self.local_rotation,
            self.global_rotation,
            self.position,
        )

    def set_pattern(self, pattern: int):
        self.pattern = pattern
        self.local_rotation.x = pattern % 4
        self.local_rotation.y = 0
        self.local_rotation.z = pattern // 4 * 2

    def set_placement(self, placement: int):
        self.placement = placement
        gr = global_rotation_for_placement(placement)
        self.global_rotation.x = gr[0]
        self.global_rotation.y = gr[1]
        self.global_rotation.z = gr[2]

    def __str__(self):
        ssss = []
        for bbbb in self._bits:
            s = ""
            for b in bbbb:
                s += "1" if b else "0"
            ssss.append(s)
        return (
            ",".join(ssss)
            + self.color
            + str(self.local_rotation)
            + str(self.global_rotation)
            + str(self.position)
        )


@app.function
def bars_to_data(bars):
    assert type(bars) == list and all(
        ["Bar" in str(type(bar)) for bar in bars]
    )
    data = []
    size = 0.99
    for bar in bars:
        for v in bar.voxels():
            data.append(
                {
                    "position": {
                        "x": v[0] + size / 2,
                        "y": v[1] + size / 2,
                        "z": v[2] + size / 2,
                    },
                    "color": bar.color,
                    "opacity": 0.9,
                    "size": {"x": size, "y": size, "z": size},
                }
            )
    return data


@app.function
def load_bars(txt: str):
    bits_list = load_txt(txt)
    bars = [Bar(bits) for bits in bits_list]

    colors = ["red", "orange", "yellow", "green", "blue", "purple"]

    for n in range(6):
        bar = bars[n]
        bar.color = colors[n]
        bar.set_placement(n)

    return bars


@app.function
def load_txt(txt) -> List[np.ndarray]:
    lines = txt.split()
    assert len(lines) == 31
    for l in lines:
        assert len(l) == 4
    bits_list = []
    for i in range(6):
        assert lines[i * 5] == "----"
        bits = np.array(
            [
                [bool(x == "1") for x in list(lines[i * 5 + 1])],
                [bool(x == "1") for x in list(lines[i * 5 + 2])],
                [bool(x == "1") for x in list(lines[i * 5 + 3])],
                [bool(x == "1") for x in list(lines[i * 5 + 4])],
            ],
            dtype=bool,
        )
        bits_list.append(bits)
    return bits_list


if __name__ == "__main__":
    app.run()
