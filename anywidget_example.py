import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import anywidget
    import traitlets

    CounterESM = """
    function render({ model, el }) {

      let button = document.createElement("button");
      button.innerHTML = `count is ${model.get("value")}`;

      button.addEventListener("click", () => {
        model.set("value", model.get("value") + 1);
        model.save_changes();
      });

      model.on("change:value", () => {
        button.innerHTML = `count is ${model.get("value")}`;
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


@app.cell
def _():
    counter_widget = CounterWidget()
    counter_widget
    return (counter_widget,)


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _(counter_widget):
    print(counter_widget.value)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
