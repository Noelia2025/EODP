# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Common auxiliary directory
auxdir = r'C:\\Users\\noeli\\Downloads\\EODP\\auxiliary'

# INPUT = E2E ISM outputs
indir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-ISM\\myoutput_e2e'

# OUTPUT = E2E L1B outputs
outdir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs_e2e'

# Initialise the L1B
myL1b = l1b(auxdir, indir, outdir)

# Execute the L1B
myL1b.processModule()