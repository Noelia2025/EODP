# TEST L1B
# Cross-validation between reference output and myoutputs

import os
import numpy as np
from netCDF4 import Dataset


# ============================================================
# PATHS
# ============================================================

reference_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1B\\output'
)

myoutput_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs'
)


# ============================================================
# FUNCTION TO FIND DATA VARIABLE
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
# CROSS VALIDATION
# ============================================================

print("")
print("==============================================")
print("              L1B CROSS VALIDATION")
print("==============================================")


for band in bands:

    print("")
    print("==============================================")
    print("BAND:", band)
    print("==============================================")

    files = [
        'l1b_toa_' + band + '.nc',
        'l1b_toa_eq_' + band + '.nc'
    ]

    for filename in files:

        reference_file = os.path.join(
            reference_dir,
            filename
        )

        my_file = os.path.join(
            myoutput_dir,
            filename
        )

        print("")
        print("----------------------------------------------")
        print(filename)

        # ----------------------------------------------------
        # CHECK FILES
        # ----------------------------------------------------

        if not os.path.exists(reference_file):

            print("Reference file not found")

            continue

        if not os.path.exists(my_file):

            print("My output file not found")

            continue


        # ----------------------------------------------------
        # READ FILES
        # ----------------------------------------------------

        reference = read_nc(
            reference_file
        )

        mine = read_nc(
            my_file
        )


        # ----------------------------------------------------
        # CHECK DIMENSIONS
        # ----------------------------------------------------

        if reference.shape != mine.shape:

            print("Different dimensions")
            print("Reference:", reference.shape)
            print("Mine:", mine.shape)

            continue


        # ----------------------------------------------------
        # DIFFERENCES
        # ----------------------------------------------------

        diff = mine - reference

        max_error = np.max(
            np.abs(diff)
        )

        mean_error = np.mean(
            np.abs(diff)
        )

        rmse = np.sqrt(
            np.mean(diff ** 2)
        )


        # ----------------------------------------------------
        # CENTRAL PIXEL
        # ----------------------------------------------------

        if reference.ndim == 2:

            ref_central = reference[50, 75]
            my_central = mine[50, 75]

        else:

            ref_central = reference.flat[0]
            my_central = mine.flat[0]


        # ----------------------------------------------------
        # PRINT RESULTS
        # ----------------------------------------------------

        print(
            "Reference [50,75]:",
            ref_central
        )

        print(
            "My output [50,75]:",
            my_central
        )

        print(
            "Max absolute error:",
            max_error
        )

        print(
            "Mean absolute error:",
            mean_error
        )

        print(
            "RMSE:",
            rmse
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if np.allclose(
            mine,
            reference,
            rtol=1e-5,
            atol=1e-8
        ):

            print(
                "RESULT: OK - MATCH"
            )

        else:

            print(
                "RESULT: DIFFERENT"
            )


print("")
print("        END OF L1B CROSS VALIDATION")