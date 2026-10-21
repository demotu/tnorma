import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from tnorma import tnorma

Y = [5, 4, 10, 8, 1, 10, 2, 7, 1, 3]


def _line(n=10):
    """Data on a line from 0 to 9: after normalization, y = 0.09*t."""
    return np.arange(n, dtype=float)


@pytest.mark.parametrize("step, n", [(1, 101), (10, 11), (-50, 50), (0, 10)])
def test_number_of_points(step, n):
    yn, tn, inds = tnorma(Y, step=step)
    assert yn.shape == tn.shape == (n,)
    assert tn[0] == 0 and tn[-1] == 100


def test_linear_interpolation_of_a_line():
    yn, tn, inds = tnorma(_line(), k=1)
    np.testing.assert_allclose(yn, 0.09*tn)
    assert inds == [0, 9]


def test_spline_passes_through_the_data():
    yn, tn, _ = tnorma(Y, step=0, k=3, smooth=0)
    np.testing.assert_allclose(yn, Y, atol=1e-10)


def test_nan_inside_the_data_is_ignored():
    y = _line()
    y[[3, 6]] = np.nan
    yn, tn, _ = tnorma(y, k=1)
    np.testing.assert_allclose(yn, 0.09*tn)


def test_nan_at_extremities_deleted():
    y = _line()
    y[[0, 1, 9]] = np.nan
    yn, tn, inds = tnorma(y, k=1, step=-8)
    assert inds == [2, 8]
    np.testing.assert_allclose(yn, np.linspace(2, 8, 8))


def test_nan_at_extremities_replaced():
    y = _line()
    y[[0, 9]] = np.nan
    yn, tn, inds = tnorma(y, k=1, step=0, nan_at_ext='replace')
    np.testing.assert_allclose(yn, [1, 1, 2, 3, 4, 5, 6, 7, 8, 8])
    assert inds == [0, 9]


def test_input_is_not_modified():
    y = _line()
    y[[0, 4]] = [np.nan, -999]
    y0 = y.copy()
    tnorma(y, k=1, mask=-999, nan_at_ext='replace')
    np.testing.assert_array_equal(y, y0)


def test_mask_with_integer_data():
    yn, tn, _ = tnorma([0, 1, 2, -999, 4, 5, 6, 7, 8, 9], k=1, mask=-999)
    np.testing.assert_allclose(yn, 0.09*tn)


def test_mask_with_list_of_values():
    y = _line()
    y[[2, 5]] = [-999, -888]
    yn, tn, _ = tnorma(y, k=1, mask=[-999, -888])
    np.testing.assert_allclose(yn, 0.09*tn)


def test_2d_columns():
    y = np.column_stack((_line(), 2*_line()))
    yn, tn, _ = tnorma(y, k=1)
    assert yn.shape == (101, 2)
    np.testing.assert_allclose(yn, np.column_stack((0.09*tn, 0.18*tn)))


def test_axis1_returns_rows():
    y = np.vstack((_line(), 2*_line(), 3*_line()))  # 3 rows x 10 samples
    yn, tn, _ = tnorma(y, axis=1, step=-5, k=1)
    assert yn.shape == (3, 5)
    for row in range(3):
        np.testing.assert_allclose(yn[row], tnorma(y[row], step=-5, k=1)[0])


def test_column_of_nans_returns_empty():
    y = np.column_stack((_line(), np.full(10, np.nan)))
    yn, tn, inds = tnorma(y)
    assert yn.size == 0 and tn.size == 0 and inds == []


def test_plot_in_given_axes():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    tnorma(Y, show=True, ax=ax1)
    assert ax1.get_xlabel() == '[%]'
    assert ax2.get_xlabel() == ''
    plt.close('all')
