#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This programs extracts density data of France provided by Insee as squares of
1km² and bins them into larger bins in order to grid them and use data in a
numpy array for further plotting. It outputs .py files of "binned" data

data source:
http://www.insee.fr/fr/themes/detail.asp?reg_id=0&ref_id=donnees-carroyees&page=donnees-detaillees/donnees-carroyees/donnees-carroyees-km.htm
"""

import dbf
import numpy as np
import gridding


def main():
    # connect to dbf database
    carreaux = dbf.Table("R_rfl09_LAEA1000.dbf")
    # print general information on db
    print carreaux

    # open the database
    carreaux.open()
    # get total number of rows
    total_count = carreaux.bottom()

    # instantiate arrays to extract data
    x = np.zeros(total_count)
    y = np.zeros(total_count)
    density = np.zeros(total_count)

    # read through database and extract data into numpy arrays
    print "Extracting data"
    i = 0
    for carre in carreaux:
        xi = carre.x_laea
        yi = carre.y_laea
        # get rid of empty rows (such as carreaux[0])
        # actually this treats the only special case which is carreaux[0]
        if xi is not None and yi is not None:
            x[i] = xi
            y[i] = yi
            density[i] = carre.ind
        i += 1

    # since I know I did not add carreaux[0].{x_laea, y_laea, ind},
    # to the arrays of saved data, I get rid of first items of each
    # array
    x = x[1:]
    y = y[1:]
    density = density[1:]

    # We have data on an unstructured mesh, let's grid the data
    # We use a simple approach: binning, for the sake of efficiency
    # It is anyhow impossible to grid all the data without some kind
    # of clustering or binning filtering step. 

    # number of bins in one direction
    n_bins = 1000.0
    # => total number of bins = (n_bins)**2

    # array geographical extent
    x_max = x.max()
    x_min = x.min()
    # y_max = y.max()
    # y_min = y.min()

    # size of a bin (length of one side of square)
    binsize = (x_max - x_min)/n_bins

    # binning, same as clustering, each bin has the mean density of all the
    # enclosed squares
    print "Binning data"
    grid, bins, binloc = gridding.griddata(x, y, density, binsize=binsize)

    # save the results to .npy files for further use
    np.save("grid.npy", grid)
    np.save("bins.npy", bins)


if __name__ == "__main__":
    main()
