# TEST L1B - EQUALIZATION EFFECT
# Compare input DN before equalization vs equalized DN
# Central row (row 50) for VNIR-0, VNIR-1, VNIR-2 and VNIR-3

import os
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# ============================================================
# PATHS
# ============================================================

# Input to L1B: final DN produced by ISM
input_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1B\\input'
)

# Our equalized L1B outputs
myoutput_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs'
)


# ============================================================
# FUNCTION TO FIND DATA VARIABLE IN NETCDF
# ============================================================

def find_data_variable(group):

    ignored_names = [
        'lat',
        'latitude',
        'lon',
        'longitude',
        'x',
        'y'
    ]

    for name in group.variables:

        if name.lower() not in ignored_names:

            return np.array(
                group.variables[name][:]
            )

    for subgroup in group.groups.values():

        result = find_data_variable(subgroup)

        if result is not None:
            return result

    return None


# ============================================================
# READ NETCDF
# ============================================================

def read_nc(filename):

    nc = Dataset(filename, 'r')

    data = find_data_variable(nc)

    nc.close()

    if data is None:
        raise ValueError(
            "No data variable found in: " + filename
        )

    return data


# ============================================================
# BANDS
# ============================================================

bands = [
    'VNIR-0',
    'VNIR-1',
    'VNIR-2',
    'VNIR-3'
]


# ============================================================
# CENTRAL ROW
# ============================================================

central_row = 50


# ============================================================
# PLOTS
# ============================================================

for band in bands:

    # --------------------------------------------------------
    # Input before equalization
    # --------------------------------------------------------

    input_file = os.path.join(
        input_dir,
        'ism_toa_' + band + '.nc'
    )

    toa_before = read_nc(
        input_file
    )


    # --------------------------------------------------------
    # Output after equalization
    # --------------------------------------------------------

    equalized_file = os.path.join(
        myoutput_dir,
        'l1b_toa_eq_' + band + '.nc'
    )

    toa_equalized = read_nc(
        equalized_file
    )


    # --------------------------------------------------------
    # Central row
    # --------------------------------------------------------

    before_row = toa_before[
        central_row,
        :
    ]

    equalized_row = toa_equalized[
        central_row,
        :
    ]


    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(
        figsize=(11, 6)
    )

    plt.plot(
        before_row,
        label='Before equalization',
        linewidth=1.5
    )

    plt.plot(
        equalized_row,
        label='After equalization',
        linewidth=1.5
    )

    plt.xlabel(
        'ACT pixel'
    )

    plt.ylabel(
        'Digital Number [DN]'
    )

    plt.title(
        'Equalization Effect - ' + band + ' - Central Row'
    )

    plt.legend()

    plt.grid()

    plt.tight_layout()


# ============================================================
# SHOW ALL FIGURES
# ============================================================

plt.show()