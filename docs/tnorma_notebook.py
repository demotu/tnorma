# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "scipy",
#     "tnorma",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # tnorma

    A Python module for temporal normalization (from 0 to 100% with step interval).

    [https://pypi.org/project/tnorma](https://pypi.org/project/tnorma)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Temporal (or time) normalization is usually employed for the temporal alignment of cyclic data obtained from different trials with different duration (number of points). The most simple and common procedure for time normalization used in Biomechanics and Motor Control is known as the normalization to percent cycle (although it might not be the most adequate procedure in certain cases ([Helwig et al., 2011](https://doi.org/10.1016/j.jbiomech.2010.09.015))).

    In the percent cycle, a fixed number (typically a temporal base from 0 to 100%) of new equally spaced data is created based on the old data with a mathematical procedure known as interpolation.
    **Interpolation** is the estimation of new data points within the range of known data points. This is different from **extrapolation**, the estimation of data points outside the range of known data points.
    Temporal normalization of data using interpolation is a simple procedure and it doesn't matter if the original data have more or less data points than desired.

    The function `tnorma.py` ([source code](https://github.com/demotu/tnorma/blob/master/tnorma/tnorma.py)) of the Python module `tnorma` implements the normalization to percent cycle procedure for temporal normalization. The function signature is:
    ```python
    yn, tn, indie = tnorma(y, axis=0, step=1, k=3, smooth=0, mask=None,
                           nan_at_ext='delete', show=False, ax=None)
    ```
    Let's see now how to perform interpolation and temporal normalization; first let's import the necessary Python libraries and configure the environment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installation

    ```bash
    pip install "tnorma[plot]"
    ```

    Or

    ```bash
    conda install -c duartexyz tnorma
    ```

    To run this [marimo](https://marimo.io) notebook in an isolated environment with all its dependencies:

    ```bash
    uvx marimo edit --sandbox tnorma_notebook.py
    ```
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    from tnorma import tnorma

    return mo, np, plt, tnorma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linear interpolation

    For instance, consider the data shown next. The temporal normalization of these data to represent a cycle from 0 to 100%, with a step of 1% (101 data points) is:
    """)
    return


@app.cell
def _():
    y = [5, 4, 10, 8, 1, 10, 2, 7, 1, 3]
    y
    return (y,)


@app.cell
def _(np, y):
    t = np.linspace(0, 100, len(y))  # time vector for the original data
    tn = np.linspace(0, 100, 101)     # new time vector for the new time-normalized data
    yn = np.interp(tn, t, y)          # new time-normalized data
    yn
    return t, tn, yn


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The key is the NumPy `interp` function, from its help:

    > interp(x, xp, fp, left=None, right=None)
    > One-dimensional linear interpolation.
    > Returns the one-dimensional piecewise linear interpolant to a function with given values at discrete data-points.

    A plot of the data will show what we have done:
    """)
    return


@app.cell
def _(plt, t, tn, y, yn):
    _fig, _ax = plt.subplots(figsize=(9, 5))
    _ax.plot(t, y, 'bo-', lw=2, label='original data')
    _ax.plot(tn, yn, '.-', color=[1, 0, 0, .5], lw=2, label='time normalized')
    _ax.legend(loc='best', framealpha=.5)
    _ax.set_xlabel('Cycle [%]')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The function `tnorma`

    The function `tnorma.py` implements this kind of normalization with options for a different interpolation than the linear one used, deal with missing points in the data (if these missing points are not at the extremities of the data because the interpolation function can not extrapolate data), and other things.
    Let's see the `tnorma.py` examples.

    Default options: cubic spline interpolation passing through each datum, 101 points, and no plot:
    """)
    return


@app.cell
def _(tnorma, y):
    tnorma(y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Linear interpolation passing through each datum:
    """)
    return


@app.cell
def _(tnorma, y):
    tnorma(y, k=1, smooth=0, mask=None, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Cubic spline interpolation with smoothing:
    """)
    return


@app.cell
def _(tnorma, y):
    tnorma(y, k=3, smooth=1, mask=None, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Cubic spline interpolation with smoothing and 50 points:
    """)
    return


@app.cell
def _(np, tnorma):
    _x = np.linspace(-3, 3, 60)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(60)/10
    tnorma(_y, step=-50, k=3, smooth=1, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Missing data

    Deal with missing data (NaNs); the first ten points are deleted (they are at the extremity) and other missing points are ignored:
    """)
    return


@app.cell
def _(np, tnorma):
    _x = np.linspace(-3, 3, 100)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(100)/10
    _y[:10] = np.nan  # first ten points are missing
    _y[30:41] = np.nan  # make other 10 missing points
    tnorma(_y, step=-50, k=3, smooth=1, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Deal with missing data at the extremities replacing by first/last not-NaN, with a cubic spline:
    """)
    return


@app.cell
def _(np, tnorma):
    _x = np.linspace(-3, 3, 100)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(100)/10
    _y[0:10] = np.nan  # first ten points are missing
    _y[-10:] = np.nan  # last ten points are missing
    tnorma(_y, step=-50, k=3, smooth=1, nan_at_ext='replace', show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And with linear interpolation:
    """)
    return


@app.cell
def _(np, tnorma):
    _x = np.linspace(-3, 3, 100)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(100)/10
    _y[0:10] = np.nan  # first ten points are missing
    _y[-10:] = np.nan  # last ten points are missing
    tnorma(_y, step=-50, k=1, smooth=0, nan_at_ext='replace', show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2-D arrays

    The data in each column are normalized (or in each row, with `axis=1`):
    """)
    return


@app.cell
def _(np, tnorma):
    _x = np.linspace(-3, 3, 100)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(100)/10
    _y = np.vstack((_y - 1, _y[::-1])).T
    _yn, _tn, _ = tnorma(_y, step=-50, k=3, smooth=1, show=True)
    print('Shape of the data:', _y.shape, ' shape of the normalized data:', _yn.shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Change the interpolation and see the temporal normalization of data with missing points (NaNs) at the beginning and in the middle of the data:
    """)
    return


@app.cell
def _(mo):
    k = mo.ui.slider(1, 5, value=3, label='k (spline degree)', show_value=True)
    smooth = mo.ui.slider(0, 5, step=0.1, value=1, label='smooth', show_value=True)
    npoints = mo.ui.slider(10, 201, value=101, label='number of points', show_value=True)
    nan_at_ext = mo.ui.dropdown(['delete', 'replace'], value='delete', label='nan_at_ext')
    mo.hstack([mo.vstack([k, smooth]), mo.vstack([npoints, nan_at_ext])],
              justify='start', gap=4)
    return k, nan_at_ext, npoints, smooth


@app.cell
def _(k, nan_at_ext, np, npoints, smooth, tnorma):
    _x = np.linspace(-3, 3, 100)
    _y = np.exp(-_x**2) + np.random.default_rng(42).standard_normal(100)/10
    _y[:10] = np.nan
    _y[30:41] = np.nan
    tnorma(_y, step=-npoints.value, k=k.value, smooth=smooth.value,
           nan_at_ext=nan_at_ext.value, show=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Helwig NE, Hong S, Hsiao-Wecksler ET, Polk JD (2011) [Methods to temporally align gait cycle data](https://doi.org/10.1016/j.jbiomech.2010.09.015). Journal of Biomechanics, 44, 561-566.
    """)
    return


if __name__ == "__main__":
    app.run()
