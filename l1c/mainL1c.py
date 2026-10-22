# MAIN FUNCTION TO CALL THE L1C MODULE

from l1c.src.l1c import l1c

# Common auxiliary directory
auxdir = r'C:\\Users\\noeli\\Downloads\\EODP\\auxiliary'

# Input directories:
# 1) E2E GM output
# 2) E2E L1B output
indir = (
    r'C:\\Users\\noeli\\Downloads\\SHARED-20260917T171805Z-1-001\\SHARED\\EODP-TS-E2E\\gm_out'
    + ','
    + r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs_e2e'
)

# Output directory
outdir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1C\\myoutput_e2e'

# Initialise the L1C module
myL1c = l1c(auxdir, indir, outdir)

# Execute the L1C module
myL1c.processModule()