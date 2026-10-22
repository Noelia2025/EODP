import os
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# ============================================================
# INPUT / OUTPUT
# ============================================================

input_dir = (
    r'C:\Users\noeli\Downloads\EODP_TER_2021-20260910T141241Z-1-001'
    r'\EODP_TER_2021\EODP-TS-L1B\myoutputs_newparams'
)

output_dir = (
    r'C:\Users\noeli\Downloads\EODP_TER_2021-20260910T141241Z-1-001'
    r'\EODP_TER_2021\EODP-TS-L1B\validation\e2e_histograms'
)

os.makedirs(output_dir, exist_ok=True)


def read_toa(filename):

    nc = Dataset(filename, 'r')

    toa = np.array(nc.variables['toa'][:])

    nc.close()

    toa = toa.flatten()
    toa = toa[np.isfinite(toa)]

    return toa


for band in range(4):

    band_name = f'VNIR-{band}'

    filename = os.path.join(
        input_dir,
        f'l1b_toa_{band_name}.nc'
    )

    toa = read_toa(filename)

    print("")
    print("==============================================")
    print(band_name)
    print("==============================================")
    print("Number of pixels:", len(toa))
    print("Min:", np.min(toa))
    print("Max:", np.max(toa))
    print("Mean:", np.mean(toa))

    plt.figure(figsize=(9, 6))

    plt.hist(
        toa,
        bins=512
    )

    plt.xlabel('Pixel Value [mW/m²/sr]')
    plt.ylabel('Frequency')
    plt.title(f'L1B TOA Radiance Histogram - {band_name}')

    plt.grid(True)

    output_file = os.path.join(
        output_dir,
        f'L1B_TOA_Histogram_{band_name}.png'
    )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

    print("Saved:", output_file)


print("")
print("ALL L1B HISTOGRAMS GENERATED")