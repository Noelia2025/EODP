# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\noeli\\Downloads\\EODP\\auxiliary'

# INPUT = ISM outputs generated with the new parameters
indir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-ISM\\myoutput_newparams'
)

# OUTPUT = L1B results generated with the new gains
outdir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001'
    r'\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs_newparams'
)

# Initialise the L1B
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()