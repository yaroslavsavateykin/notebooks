import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import mpl_typst
    import numpy as np
    import pandas as pd
    from unc_tools import UncRegression, serif

    return UncRegression, pd, plt, serif


@app.cell
def _(pd):
    df = pd.DataFrame({})

    df["C_Na"] = [2.5, 5, 10, 15, 20]
    df["I_Na"] = [16, 25, 41, 51, 66]

    df["C_K"]  = [1, 2, 3, 4, 5]
    df["I_K"] = [139,264, 388, 515, 632]

    df["C_Ca"] = [0.1, 0.2, 0.3, 0.4, 0.5]
    df["I_Ca"] = [32, 62, 93, 125, 155]

    control_dict = {"Na": 44, "K": 433, "Ca": 71}

    df
    return control_dict, df


@app.cell
def _(UncRegression, control_dict, df, plt, serif):
    import unc_tools.patches
    serif()

    fig, axes = plt.subplots(1,3,figsize=(15,5), dpi=200)
    axes = axes.flatten()
    result = []

    for i, name in enumerate(control_dict.keys()):

        C = df[f"C_{name}"]
        I = df[f"I_{name}"]
        y0 = control_dict[name]
        ax = axes[i]

        reg = UncRegression(C,I)
        # Solve for concentration at the control current.
        x0 = reg.find_x(y0)
        result.append(x0)

        reg.plot(ax=ax, show_band=True)
        ax.scatter(x0,y0, label = "Control")

    #    ax.text(x0.n*1.1,y0,f"$({x0})$".replace("+/-", "\\pm"))
        ax.text(x0.n*1.1,y0,f"$({x0})$")
        ax.set_xlabel("C, $\\mu$g/ml")
        ax.set_ylabel("I")
        ax.set_title(name)
        ax.legend()

    fig.savefig("test.typ")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
