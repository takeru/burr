import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    from data import load_bars, Bar, bars_to_data
    from threejs import ThreeWidget
    import marimo as mo
    return ThreeWidget, bars_to_data, load_bars, mo


@app.cell
def _(ThreeWidget, load_bars, mo):
    pat = mo.ui.slider(start=0, stop=7)
    ofs = mo.ui.slider(start=0, stop=10, step=0.2)

    bars = load_bars(blue_puzzle_txt())
    widget = ThreeWidget()
    widget.data = []
    return bars, ofs, pat, widget


@app.cell
def _(widget):
    widget
    return


@app.cell
def _(mo, ofs, pat):
    mo.md(
        f"""
    - pat: {pat} {pat.value}
    - ofs: {ofs} {ofs.value}
    """
    )
    return


@app.cell
def _(bars, bars_to_data, ofs, pat, widget):
    for i, bar in enumerate(bars):
        if i == 1 or i == 3:
            bar.position.x = ofs.value
        if i == 2 or i == 4:
            bar.position.z = ofs.value

    for bar in bars:
        bar.set_pattern(pat.value)

    widget.data = bars_to_data(bars)
    return


@app.function
def blue_puzzle_txt():
    return """
----
0001
0110
1001
1111
----
0011
0011
1111
1101
----
0000
0001
1111
1101
----
1110
1100
1111
1001
----
1000
0000
1001
1111
----
0001
0011
1101
1111
----
"""


if __name__ == "__main__":
    app.run()
