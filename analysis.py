"""Analyze GHCN data.

"""
# pylint: disable=invalid-name, locally-disabled
# pylint: disable=pointless-string-statement, locally-disabled

import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

__author__ = "Phil Beffrey"
__copyright__ = "Copyright (c) 2019, Phil Beffrey"
__license__ = "MIT"
__version__ = "0.0.1"


def linear_regression(x, y):
    """Fit the {x, y} data with a line.

    """
    x_1 = np.c_[np.ones((len(x), 1)), x]  # add x0 = 1 to each instance
    z = np.linalg.inv(x_1.T.dot(x_1)).dot(x_1.T).dot(y)
    # print(z)

    x_new = np.array([[0], [len(x)]])
    x_new_1 = np.c_[np.ones((2, 1)), x_new]
    y_predict = x_new_1.dot(z)
    # print(y_predict)
    return {'x': x_new, 'y': y_predict}


def polynomial_regression(x, y, deg):
    """Fit the {x, y} data with a curve.

    """
    poly_features = PolynomialFeatures(degree=deg, include_bias=False)
    x_poly = poly_features.fit_transform(x)

    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, y)

    length = len(x)
    x_new = np.linspace(0, length - 1, length).reshape(length, 1)
    x_new_poly = poly_features.transform(x_new)
    y_new = lin_reg.predict(x_new_poly)
    return {'x': x_new, 'y': y_new}


PLOT_LAYOUT = []
PLOT_LAYOUT_INDEX = 0


def plot_years(df, id_, fit_fn, years=None):
    """Plot selected years for a station.

    """
    global PLOT_LAYOUT_INDEX
    if PLOT_LAYOUT:
        ax = PLOT_LAYOUT[PLOT_LAYOUT_INDEX]
        PLOT_LAYOUT_INDEX = (PLOT_LAYOUT_INDEX + 1) % len(PLOT_LAYOUT)
    else:
        ax = plt

    colors = ['b', 'r', 'g', 'c', 'm', 'y']
    n_plots = 0
    x = df.index.values
    for y in years:
        c = colors[n_plots % len(colors)]
        n_plots += 1
        y = df[y]
        ax.plot(x, y, snap=False, alpha=0.20, color=c)
        """
        result = linear_regression(x, y)
        plt.plot(result['x'], result['y'], 'r-')
        """

        # (!?) Sort of the same as: 'X = x.reshape(-1, 1)'
        X = []
        for i in x:
            X.append([i])

        # degree=5 seems about right for yearly TMAX data.
        # (!) But need to pad with data from prev and next years.
        result = fit_fn(X, y, 5)
        ax.plot(result['x'],
                result['y'],
                "r-",
                snap=False,
                alpha=0.35,
                color=c)

    ax.set_title(id_ + ' ' + str(years[0]) + '-' + str(years[len(years) - 1]))
    # plt.show() # Comment out to allow the *next* show() to draw.
