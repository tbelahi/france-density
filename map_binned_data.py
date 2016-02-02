#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This programs takes a .npy file containing gridded/binned data of France as
input and make maps from it which ares saved in .pdf files.
The input is computed with extract_and_bin_data.py
"""

import numpy as np
import matplotlib.pyplot as pl


def main():
    # load data
    density = np.load("grid.npy")

    # apply some useful transforms
    density = np.flipud(density)
    density = density + 1e-7       # we can apply log to density now

    # plots
    fig, axs = pl.subplots(2, 2)

    for i, cmap in enumerate(["viridis", "magma", "magma_r", "YlOrRd"]):
        k, l = i % 2, i/2
        axs[k, l].imshow(np.log(density), vmin=0, vmax=np.log(5000), cmap=cmap)
        axs[k, l].set_title(cmap)

    fig.subplots_adjust()
    fig.savefig("densite-france.pdf", dpi=300)

if __name__ == "__main__":
    main()
