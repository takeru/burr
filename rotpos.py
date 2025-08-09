import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    from threejs import ThreeWidget
    from typing import List
    from dataclasses import dataclass
    import numpy as np

    from data import Bar, bars_to_data


@app.cell
def _():
    rotation_x = mo.ui.slider(start=0, stop=3)
    rotation_y = mo.ui.slider(start=0, stop=3)
    rotation_z = mo.ui.slider(start=0, stop=3)
    rotation_xyz = mo.ui.array(elements=[rotation_x,rotation_y,rotation_z])

    return (rotation_xyz,)


@app.cell
def _(rotation_xyz):
    _bars = []
    b0 = Bar(np.array([
        [True, False, False, False],
        [False, False, False, False],
        [True, True, True, True],
        [True, True, True, True],
    ]))
    b0.rotation.x = rotation_xyz[0].value
    b0.rotation.y = rotation_xyz[1].value
    b0.rotation.z = rotation_xyz[2].value
    _bars.append(b0)

    widget01 = ThreeWidget()
    widget01.data = bars_to_data(_bars)
    [widget01, rotation_xyz]
    return


if __name__ == "__main__":
    app.run()
