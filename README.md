# [tnorma](https://pypi.org/project/tnorma/)

[![PyPI version](https://badge.fury.io/py/tnorma.svg)](https://badge.fury.io/py/tnorma)
[![DOI](https://zenodo.org/badge/251048661.svg)](https://zenodo.org/badge/latestdoi/251048661)

Temporal normalization (from 0 to 100% with step interval).

Temporal normalization is usually employed for the temporal alignment of data obtained from different trials with different duration (number of points). This code implements a procedure knwown as the normalization to percent cycle.

This code can perform simple linear interpolation passing through each datum or spline interpolation (up to quintic splines) passing through each datum (knots) or not (in case a smoothing parameter > 0 is inputted).

NaNs and any value inputted as a mask parameter and that appears at the extremities might be removed or replaced by the first/last not-NaN value before the interpolation because this code does not perform extrapolation.  
For a 2D array, the entire row with NaN or a mask value at the extermity might be removed because of alignment issues with the data from different columns. As result, if there is a column of only NaNs in the data, the temporal normalization can't be performed (an empty NaNs and any value inputted as a mask parameter and that appears in the middle of the data (which may represent missing data) are ignored and the interpolation is performed through these points.

## Installation

```bash
pip install tnorma
```

Or

```bash
conda install -c duartexyz tnorma
```

## Examples

```python
>>> # Default options: cubic spline interpolation passing through
>>> # each datum, 101 points, and no plot
>>> y = [5,  4, 10,  8,  1, 10,  2,  7,  1,  3]
>>> tnorma(y)

>>> # Deal with missing data (use NaN as mask)
>>> x = np.linspace(-3, 3, 100)
>>> y = np.exp(-x**2) + np.random.randn(100)/10
>>> y[:10] = np.NaN # first ten points are missing
>>> y[30: 41] = np.NaN # make other 10 missing points
>>> yn, tn, indie = tnorma(y, step=-50, k=3, smooth=1, show=True)

>>> # Deal with 2-D array
>>> x = np.linspace(-3, 3, 100)
>>> y = np.exp(-x**2) + np.random.randn(100)/10
>>> y = np.vstack((y-1, y[::-1])).T
>>> yn, tn, indie = tnorma(y, step=-50, k=3, smooth=1, show=True)
```

- [tnorma.ipynb](https://github.com/demotu/tnorma/blob/master/docs/tnorma.ipynb)

## How to cite this work

Here is a suggestion to cite this GitHub repository:

> Marcos Duarte. (2021). tnorma: A Python module for temporal normalization (from 0 to 100% with step interval) (Version v0.0.3). Zenodo. http://doi.org/10.5281/zenodo.4599136

And a possible BibTeX entry:

```tex
@software{marcos_duarte_2021_4599136,
  author       = {Marcos Duarte},
  title        = {{tnorma: A Python module for temporal normalization 
                   (from 0 to 100\% with step interval)}},
  month        = mar,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v0.0.3},
  doi          = {10.5281/zenodo.4599136},
  url          = {https://doi.org/10.5281/zenodo.4599136}
}
```

## License

The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
