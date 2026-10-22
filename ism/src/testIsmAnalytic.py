# TEST ISM - ANALYTIC vs READ
# Validation of pixel TOA[50,75] for all VNIR bands

import os
import numpy as np
from netCDF4 import Dataset

from config.ismConfig import ismConfig



# PATH


myoutput_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-ISM\\myoutput'
)


# ============================================================
# PIXEL TO VALIDATE
# ============================================================

row = 50
column = 75


# ============================================================
# CONFIGURATION
# ============================================================

config = ismConfig()


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
            "No data variable found in " + filename
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
# CONSTANTS
# ============================================================

h = 6.62606896e-34
c = 2.99792458e8

pixel_area = config.pix_size ** 2

max_dn = 2 ** config.bit_depth - 1


# ============================================================
# VALIDATION
# ============================================================

print("")
print("==========================================================")
print("           ISM ANALYTIC vs READ - TOA[50,75]")
print("==========================================================")


for band_index, band in enumerate(bands):

    print("")
    print("==========================================================")
    print("BAND:", band)
    print("==========================================================")

    # --------------------------------------------------------
    # FILES
    # --------------------------------------------------------

    optical_file = os.path.join(
        myoutput_dir,
        'ism_toa_optical_' + band + '.nc'
    )

    electrons_file = os.path.join(
        myoutput_dir,
        'ism_toa_e_' + band + '.nc'
    )

    detection_file = os.path.join(
        myoutput_dir,
        'ism_toa_detection_' + band + '.nc'
    )

    dn_file = os.path.join(
        myoutput_dir,
        'ism_toa_' + band + '.nc'
    )


    # --------------------------------------------------------
    # READ OUTPUTS
    # --------------------------------------------------------

    optical = read_nc(optical_file)

    electrons = read_nc(electrons_file)

    detection = read_nc(detection_file)

    dn = read_nc(dn_file)


    # ========================================================
    # 1. IRRADIANCE - READ
    # ========================================================

    irradiance_read = optical[row, column]


    # ========================================================
    # 2. IRRADIANCE -> PHOTONS - ANALYTIC
    # ========================================================

    wavelength = config.wv[band_index]

    # Optical output is in mW/m2
    irradiance_W = irradiance_read * 1e-3

    # Energy reaching the detector
    energy = (
        irradiance_W
        * pixel_area
        * config.t_int
    )

    # Energy of one photon
    photon_energy = (
        h * c / wavelength
    )

    # Number of photons
    photons_analytic = (
        energy / photon_energy
    )


    # ========================================================
    # 3. PHOTONS -> ELECTRONS - ANALYTIC
    # ========================================================

    electrons_before_saturation = (
        photons_analytic * config.QE
    )

    # Apply Full Well Capacity
    electrons_analytic = min(
        electrons_before_saturation,
        config.FWC
    )

    # Read value from ISM output
    electrons_read = electrons[row, column]


    # ========================================================
    # 4. DETECTION OUTPUT - READ
    # ========================================================

    detection_read = detection[row, column]


    # ========================================================
    # 5. ELECTRONS -> VOLTAGE - ANALYTIC
    # ========================================================

    voltage_analytic = (
        detection_read
        * config.OCF
        * config.ADC_gain
    )


    # ========================================================
    # 6. VOLTAGE -> DN - ANALYTIC
    # ========================================================

    dn_analytic = np.round(
        (
            voltage_analytic
            - config.min_voltage
        )
        /
        (
            config.max_voltage
            - config.min_voltage
        )
        *
        max_dn
    )

    # ADC saturation
    if dn_analytic > max_dn:
        dn_analytic = max_dn

    if dn_analytic < 0:
        dn_analytic = 0


    # Read final DN
    dn_read = dn[row, column]


    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print("")

    print(
        "Irradiance READ [mW/m2]:",
        irradiance_read
    )

    print(
        "Wavelength [m]:",
        wavelength
    )

    print(
        "Photons ANALYTIC [ph]:",
        photons_analytic
    )

    print("")

    print(
        "Electrons before FWC [e-]:",
        electrons_before_saturation
    )

    print(
        "Electrons ANALYTIC [e-]:",
        electrons_analytic
    )

    print(
        "Electrons READ [e-]:",
        electrons_read
    )

    print(
        "Electron difference:",
        electrons_read - electrons_analytic
    )

    print("")

    print(
        "Detection READ [e-]:",
        detection_read
    )

    print(
        "Voltage ANALYTIC [V]:",
        voltage_analytic
    )

    print("")

    print(
        "DN ANALYTIC:",
        dn_analytic
    )

    print(
        "DN READ:",
        dn_read
    )

    print(
        "DN difference:",
        dn_read - dn_analytic
    )

    print("")

    if np.isclose(
        electrons_read,
        electrons_analytic,
        rtol=1e-5,
        atol=1e-5
    ):

        print(
            "Electrons result: OK - MATCH"
        )

    else:

        print(
            "Electrons result: DIFFERENT"
        )


    if dn_read == dn_analytic:

        print(
            "DN result: OK - MATCH"
        )

    else:

        print(
            "DN result: DIFFERENT"
        )


print("")
print("          END ISM ANALYTIC VALIDATION")