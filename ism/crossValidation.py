import os
import numpy as np
from netCDF4 import Dataset


# Output de referencia de la profesora
reference_dir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-ISM\\output'

# Mi output
myoutput_dir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-ISM\\myoutput'


def read_toa(filename):

    dataset = Dataset(filename, 'r')

    toa = dataset.variables['toa'][:]

    dataset.close()

    return np.array(toa)


# Buscar archivos .nc de referencia
files = [
    f for f in os.listdir(reference_dir)
    if f.endswith('.nc')
]

print("==============================================")
print("         CROSS VALIDATION ISM")
print("==============================================")

for filename in files:

    reference_file = os.path.join(reference_dir, filename)
    my_file = os.path.join(myoutput_dir, filename)

    print("\n----------------------------------------------")
    print(filename)

    # Comprobar que existe también en myoutput
    if not os.path.exists(my_file):

        print("NO EXISTE EN MYOUTPUT")

        continue

    reference = read_toa(reference_file)
    mine = read_toa(my_file)

    # Comprobar dimensiones
    if reference.shape != mine.shape:

        print("ERROR: dimensiones diferentes")
        print("Profesor:", reference.shape)
        print("Mío:", mine.shape)

        continue

    # Diferencias
    difference = mine - reference

    max_error = np.max(np.abs(difference))
    mean_error = np.mean(np.abs(difference))
    rmse = np.sqrt(np.mean(difference ** 2))

    print("Shape:", mine.shape)
    print("Profesor [0,0]:", reference[0, 0])
    print("Mío     [0,0]:", mine[0, 0])
    print("Error máximo:", max_error)
    print("Error medio:", mean_error)
    print("RMSE:", rmse)

print("\n==============================================")
print("       FIN CROSS VALIDATION")
print("==============================================")