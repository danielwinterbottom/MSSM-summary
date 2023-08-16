# Inputs used for this recast. Numbers obtained from: 
# https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHWG/Higgs_XSBR_YR4_update.xlsx
# https://pdg.lbl.gov/2022/listings/contents_listings.html
mh         = 125.4                  # Observed H(125) mass
br_2l2n    = 1.086e-1**2            # BR(H(125)->W(lnu)W(lnu)

import csv
# Set up the model
import mssm_xs_tools 
mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/mh125EFT_13.root", True, 0)
def ggHWW(mA, tb): 
    return mssm.xsec(b"gg->H", mA, tb)*mssm.br(b"H->WW", mA, tb)
def mH2mA(mX, tb):
    return mssm.mass2mA(b"H", mX, tb)
# Set up the scan
start = 60
stop  = 0.5
step  =-0.5

def recast_limits(source, target, mass_column, limit_column, br_WW=1.): 
    # Read
    contour = []
    from mssm_extra_tools import mA_tanb_scan
    with open(source) as f:
        r=csv.DictReader(f, delimiter=",")
        for l in r:
            contour.append(mA_tanb_scan(float(l[limit_column])/br_WW, float(l[mass_column]), 
            mH2mA, ggHWW, start, stop, step))
    # Write
    with open(target, mode="w") as f:
        w=csv.writer(f, delimiter=",")
        w.writerow(["mA","tanb"])
        for l in contour:
            if not l[1]==stop:
                w.writerow(l)

if __name__=="__main__":
    #recast_limits("./csv_files/HIG-20-016_obs.csv", "./csv_files/HIG-20-016_mAtanb_obs.csv", "mX", "limit", br_2l2n)
    #recast_limits("./csv_files/HIG-20-016_exp.csv", "./csv_files/HIG-20-016_mAtanb_exp.csv", "mX", "limit", br_2l2n)
    # The old (and published) limit the partial Run-2 data
    recast_limits("./csv_files/HIG-17-033_obs.csv", "./csv_files/HIG-17-033_mAtanb_obs.csv", "mX", "limit")
    recast_limits("./csv_files/HIG-17-033_exp.csv", "./csv_files/HIG-17-033_mAtanb_exp.csv", "mX", "limit")

