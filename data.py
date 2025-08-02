import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")


@app.cell
def _():
    blue_puzzle = """
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
    return (blue_puzzle,)


@app.class_definition
class Bar:
    def __init__(self, bits):
        self._bits = bits

    def __str__(self):
        ssss = []
        for bbbb in self._bits:
            s = ""
            for b in bbbb:
                s += "1" if b else "0"
            ssss.append(s)
        return ",".join(ssss)


@app.cell
def _(blue_puzzle):
    class Puzzle:
        def __init__(self, txt):
            self._bars = []
            self._load(txt)

        def _load(self, txt):
            lines = txt.split()
            assert len(lines) == 31
            for l in lines:
                assert len(l) == 4
            for i in range(6):
                assert lines[i*5] == "----"
                bar = Bar([
                    [bool(x=="1") for x in list(lines[i*5+1])],
                    [bool(x=="1") for x in list(lines[i*5+2])],
                    [bool(x=="1") for x in list(lines[i*5+3])],
                    [bool(x=="1") for x in list(lines[i*5+4])]
                ])
                self._bars.append(bar)

        @property
        def bars(self):
            return self._bars

        def __str__(self):
            return str([str(bar) for bar in self._bars])

        def __repr__(self):
            return f"Puzzle({self})"

    puzzle = Puzzle(blue_puzzle)
    puzzle
    return (puzzle,)


@app.cell
def _(ThreeWidget, puzzle):
    _data = []

    colors = ["red", "orange", "yellow", "green", "blue", "purple"]

    for bar_no, bar in enumerate(puzzle.bars):
        for i, bbbb in enumerate(bar._bits):
            y = 1 - (i//2)
            z = i % 2 + (4 * (bar_no-2.5))
            for x, b in enumerate(bbbb):
                if b:
                    _data.append(
                        {"position": {"x": x, "y": y, "z": z},
                         "color": colors[bar_no],
                         "opacity": 0.8,
                         "size": {"x": 0.9, "y": 0.9, "z": 0.9}},
                    )

    puzzle_widget = ThreeWidget()
    puzzle_widget.data = _data
    [puzzle_widget, _data]

    return


@app.cell
def _():
    import marimo as mo
    from threejs import ThreeWidget
    return (ThreeWidget,)


if __name__ == "__main__":
    app.run()
