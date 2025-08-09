import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    from dataclasses import dataclass


@app.class_definition
@dataclass
class Foo:
    a: int


@app.class_definition
@dataclass
class Boo:
    b: int


@app.function
def baz(n):
    return n * 2


@app.cell
def _():
    class Bar:
        def __init__(self):
            self.foo = Foo(123)
            self.foo.a = baz(123)
            self.boo = Boo(789)
            self.boo.b = baz(999)

        def asdf2(self):
            hjkl()
    return (Bar,)


@app.cell
def _(Bar):
    bar = Bar()
    bar.foo.a
    return


@app.cell
def _(Bar, zzz):
    def asdf():
        b = Bar()
        print(zzz)
        print(b)
        return [b]
    return (asdf,)


@app.cell
def _():
    zzz = "ZZZ"
    return (zzz,)


@app.cell
def _(asdf):
    asdf()
    return


@app.function
def hjkl():
    pass


if __name__ == "__main__":
    app.run()
