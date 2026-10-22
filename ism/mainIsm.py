# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Common auxiliary directory
auxdir = r'C:\\Users\\noeli\\Downloads\\EODP\\auxiliary'

# E2E input from SGM output
indir = r'C:\\Users\\noeli\\Downloads\\SHARED-20260917T171805Z-1-001\\SHARED\\EODP-TS-E2E\\sgm_out'

# E2E ISM output
outdir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-ISM\\myoutput_e2e'

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)

# Execute the ISM
myIsm.processModule()