import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import anywidget
    import traitlets

    CounterESM = """
    function render({ model, el }) {

      let button = document.createElement("button");

      button.addEventListener("click", () => {
        model.set("value", model.get("value") + 1);
        model.save_changes();
      });

      const updateInnerHTML = ()=>{
        button.innerHTML = `count=${model.get("value")} data=${model.get("data")}`;
      }
      updateInnerHTML();

      model.on("change:value", () => {
        updateInnerHTML();
      });

      model.on("change:data", () => {
        updateInnerHTML();
      });

      el.appendChild(button);
    }
    export default { render };
    """


@app.class_definition
class CounterWidget(anywidget.AnyWidget):
    _esm = CounterESM
    # Stateful property that can be accessed by JavaScript & Python
    value = traitlets.Int(0).tag(sync=True)
    data = traitlets.List([1, 2, 3]).tag(sync=True)


@app.cell
def _(mo):
    count_slider = mo.ui.slider(start=0, stop=100)
    return (count_slider,)


@app.cell
def _():
    counter_widget = CounterWidget()
    return (counter_widget,)


@app.cell
def _(count_slider, counter_widget):
    counter_widget.value = count_slider.value
    return


@app.cell
def _(count_slider, counter_widget, mo):
    mo.md(
        f"""
    - {counter_widget}
    - {count_slider}
    - {count_slider.value}
    """
    )
    return


@app.cell
def _():
    # [counter_widget,count_slider]
    # mo.ui.array(elements=[counter_widget,count_slider])
    return


@app.cell
def _(count_slider):
    count_slider
    return


@app.cell
def _():
    # counter_widget.value = 100
    return


@app.cell
def _():
    # counter_widget.data = [2, 3]
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    # print(counter_widget.value)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
