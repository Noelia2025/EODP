# MAIN FUNCTION TO CALL THE L1C MODULE

from l1c.src.l1c import l1c


# Directory - common directory for the execution of the E2E
auxdir = r'C:\\Users\\noeli\\Downloads\\EODP\\auxiliary'


# Input directories:
# 1) GM output
# 2) Our L1B output generated with the new parameters
indir = (
    r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1C\\input\\gm_alt100_act_150'
    + ','
    + r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1B\\myoutputs_newparams'
)


# Output directory for the new chained execution
outdir = r'C:\\Users\\noeli\\Downloads\\EODP_TER_2021-20260910T141241Z-1-001\\EODP_TER_2021\\EODP-TS-L1C\\myoutput_newparams'


# Initialise the L1C module
myL1c = l1c(auxdir, indir, outdir)


# Execute the L1C module
myL1c.processModule()