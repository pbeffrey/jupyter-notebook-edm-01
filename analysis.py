"""Analyze GHCN data.

"""
# pylint: disable=invalid-name, locally-disabled
# pylint: disable=pointless-string-statement, locally-disabled

import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def linear_regression(x, y):
    """Just what it says.

    """
    x_b = np.c_[np.ones((len(x), 1)), x]  # add x0 = 1 to each instance
    z = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(y)
    # print(z)

    x_new = np.array([[0], [len(x)]])
    x_new_b = np.c_[np.ones((2, 1)), x_new]
    y_predict = x_new_b.dot(z)
    # print(y_predict)
    return {'x': x_new, 'y': y_predict}


def polynomial_regression(x, y, deg):
    """Just what it says.

    """
    poly_features = PolynomialFeatures(degree=deg, include_bias=False)
    x_poly = poly_features.fit_transform(x)

    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, y)

    x_new = np.linspace(0, 365, 366).reshape(366, 1)
    x_new_poly = poly_features.transform(x_new)
    y_new = lin_reg.predict(x_new_poly)
    return {'x': x_new, 'y': y_new}


PLOT_LAYOUT = []
PLOT_LAYOUT_INDEX = 0


def plot_years(df, id_, years=None):
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
        result = polynomial_regression(X, y, 5)
        ax.plot(result['x'],
                result['y'],
                "r-",
                snap=False,
                alpha=0.35,
                color=c)

    ax.set_title(id_ + ' ' + str(years[0]) + '-' + str(years[len(years) - 1]))
    # plt.show() # Comment out to allow the *next* show() to draw.
