import logging

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from bfast import BFAST
from datasets import *

from setup import logging_setup


logger = logging.getLogger(__name__)


def interp_nans(x):
    x_nn = np.array(pd.DataFrame(x).interpolate().values.ravel().tolist())
    nans = x_nn[np.isnan(x)]
    return x_nn, nans


def plot(name, y, x, f, season, level=0.05, h=0.15, max_iter=10, nan_clr="crimson"):
    def segmented_plot(arr, bp):
        prev = 0
        vals = np.concatenate((bp, [arr.shape[0] - 1]))
        for i, s in enumerate(vals + 1):
            ind = max(0, prev-1)
            ax.plot(x[ind:s], arr[ind:s], label="seg {}".format(i+1))
            ax.legend()
            prev = s

    def add_nans(y_n):
        if nans:
            ax.scatter(x_n, y_n, color=nan_clr, label="missing values", marker="x")
            ax.legend()

    print("Plotting {}".format(name))
    vo = BFAST(y, x, f, season=season, level=level, h=h, max_iter=max_iter).output
    nans = np.isnan(y).any()

    x_n = x[np.isnan(y)]
    y, y_n = interp_nans(y)
    Tt, Tt_n = interp_nans(vo.trend)
    St, St_n = interp_nans(vo.season)
    Rt, Rt_n = interp_nans(vo.remainder)
    Tt_bp = vo.trend_breakpoints
    St_bp = vo.season_breakpoints


    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(name, fontsize=24)
    if season != "none":
        ax = fig.add_subplot(4, 1, 1)
        # plot Y
        ax.set_title("observations")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.plot(x, y)
        add_nans(y_n)

        # plot trend
        ax = fig.add_subplot(4, 1, 2)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title("trend")
        if Tt_bp is not None:
            segmented_plot(Tt, Tt_bp)
        else:
            ax.plot(x, Tt)
        add_nans(Tt_n)

        # plot season
        ax = fig.add_subplot(4, 1, 3)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title("season")
        if St_bp is not None:
            segmented_plot(St, St_bp)
        else:
            ax.plot(x, St)
        add_nans(St_n)

        # plot remainder
        ax = fig.add_subplot(4, 1, 4)
        ax.set_title("remainder")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.plot(x, Rt)
        add_nans(Rt_n)

    else:
        ax = fig.add_subplot(1, 1, 1)
        if Tt_bp is not None:
            prev = 0
            vals = np.concatenate((Tt_bp, [y.shape[0] - 1]))
            for i, s in enumerate(vals + 1):
                ind = max(0, prev-1)
                ax.plot(x[ind:s], y[ind:s], label="seg {}".format(i+1))
                ax.legend()
                prev = s
        else:
            ax.plot(x, Tt)

    plt.subplots_adjust(hspace=0.6)
    plt.savefig(name.lower() + ".png", bbox_inches ="tight")


if __name__ == "__main__":
    logging_setup()

    plot("harvest", harvest, harvest_dates, harvest_freq, "harmonic")
    plot("nile", nile, nile_dates, None, "none")
    plot("SIMTS", simts_sum, simts_dates, simts_freq, "harmonic", level=0.35, h=0.3, max_iter=2)
    plot("NDVI", ndvi, ndvi_dates, ndvi_freq, "dummy")
