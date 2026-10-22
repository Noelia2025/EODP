# TEST L1C
# 1) Plot L1B grid (red) versus L1C grid (blue)
# 2) Spatial Sampling Distance (Haversine) - central row
# 3) Spatial Sampling Distance (Haversine) - central column

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

from common.io.readGeodetic import readGeodetic


# ============================================================
# PATHS
# ============================================================

input_dir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1C\\input'
    r'\\gm_alt100_act_150'
)

input_filename = 'geolocation.nc'

output_file = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1C\\myoutput'
    r'\\l1c_toa_VNIR-0.nc'
)


# ============================================================
# READ L1B GRID
# ============================================================

lat_l1b, lon_l1b = readGeodetic(
    input_dir,
    input_filename
)


# ============================================================
# FUNCTION TO FIND VARIABLES INSIDE NETCDF
# ============================================================

def find_variable(group, possible_names):

    for name in possible_names:
        if name in group.variables:
            return np.array(group.variables[name][:])

    for subgroup in group.groups.values():

        result = find_variable(
            subgroup,
            possible_names
        )

        if result is not None:
            return result

    return None


# ============================================================
# READ L1C OUTPUT GRID
# ============================================================

nc = Dataset(output_file, 'r')

lat_l1c = find_variable(
    nc,
    ['lat', 'latitude', 'Latitude', 'LAT']
)

lon_l1c = find_variable(
    nc,
    ['lon', 'longitude', 'Longitude', 'LON']
)

nc.close()

if lat_l1c is None or lon_l1c is None:
    raise ValueError(
        "Latitude or longitude not found in L1C file"
    )


# ============================================================
# FIGURE 1 - L1B GRID vs L1C GRID
# ============================================================

plt.figure(figsize=(10, 8))

plt.scatter(
    lon_l1b.flatten(),
    lat_l1b.flatten(),
    c='red',
    s=5,
    label='L1B grid'
)

plt.scatter(
    lon_l1c.flatten(),
    lat_l1c.flatten(),
    c='blue',
    s=5,
    label='L1C grid'
)

plt.xlabel('Longitude [deg]')
plt.ylabel('Latitude [deg]')

plt.title(
    'L1B grid (red) versus L1C grid (blue)'
)

plt.legend()
plt.grid()


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

R = 6371000.0


def haversine(lat1, lon1, lat2, lon2):

    lat1 = np.deg2rad(lat1)
    lon1 = np.deg2rad(lon1)

    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2.0) ** 2
        +
        np.cos(lat1)
        *
        np.cos(lat2)
        *
        np.sin(dlon / 2.0) ** 2
    )

    c = 2.0 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1.0 - a)
    )

    return R * c


# ============================================================
# CENTRAL ROW
# ============================================================

central_row = int(lat_l1b.shape[0] / 2)

lat_row = lat_l1b[central_row, :]
lon_row = lon_l1b[central_row, :]

ssd_row = haversine(
    lat_row[:-1],
    lon_row[:-1],
    lat_row[1:],
    lon_row[1:]
)


# ============================================================
# FIGURE 2 - SSD CENTRAL ROW
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    np.arange(len(ssd_row)),
    ssd_row
)

plt.xlabel('Column')
plt.ylabel('Spatial Sampling Distance [m]')

plt.title(
    'Spatial Sampling Distance - Central Row of L1B Geometry'
)

plt.grid()


# ============================================================
# CENTRAL COLUMN
# ============================================================

central_column = int(lat_l1b.shape[1] / 2)

lat_column = lat_l1b[:, central_column]
lon_column = lon_l1b[:, central_column]

ssd_column = haversine(
    lat_column[:-1],
    lon_column[:-1],
    lat_column[1:],
    lon_column[1:]
)


# ============================================================
# FIGURE 3 - SSD CENTRAL COLUMN
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    np.arange(len(ssd_column)),
    ssd_column
)

plt.xlabel('Row')
plt.ylabel('Spatial Sampling Distance [m]')

plt.title(
    'Spatial Sampling Distance - Central Column of L1B Geometry'
)

plt.grid()


# ============================================================
# PRINT RESULTS
# ============================================================

print("")
print("CENTRAL ROW:", central_row)
print("Row SSD min  [m]:", np.min(ssd_row))
print("Row SSD max  [m]:", np.max(ssd_row))
print("Row SSD mean [m]:", np.mean(ssd_row))

print("")

print("CENTRAL COLUMN:", central_column)
print("Column SSD min  [m]:", np.min(ssd_column))
print("Column SSD max  [m]:", np.max(ssd_column))
print("Column SSD mean [m]:", np.mean(ssd_column))


# ============================================================
# SHOW ALL FIGURES
# ============================================================

plt.show()