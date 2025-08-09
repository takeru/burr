import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.function
def love_dozen():
    # LovesDozen https://www.cs.brandeis.edu/~storer/JimPuzzles/ZPAGES/zzz6PieceLev12LovesDozen.html
    return """
----
1000
0000
1111
1001
----
0000
0000
1111
1011
----
0010
0000
1111
1101
----
0100
0000
1111
1001
----
0101
0001
1111
1111
----
0010
0000
1111
1001
----
"""


@app.function
def without_internal_voids():
    # Six-piece burr puzzle without internal voids
    # https://www.craftsmanspace.com/free-projects/six-piece-burr-puzzles.html
    return """
----
1001
0001
1111
0001
----
1111
0000
1111
0000
----
1001
0000
1111
0110
----
1001
1000
1111
1110
----
0000
0000
1111
1001
----
1111
1111
1111
1111
----
"""


@app.function
# Six-piece burr puzzle with simple notches
# https://www.craftsmanspace.com/free-projects/six-piece-burr-puzzles.html
def simple_notches():
    return """
----
0100
0100
1111
1111
----
0000
0000
1111
1101
----
1001
1000
1111
1100
----
1100
0000
1111
1001
----
1001
0000
1111
0000
----
1111
1111
1111
1111
----
"""


if __name__ == "__main__":
    app.run()
