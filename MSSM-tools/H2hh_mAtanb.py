# Inputs used for this recast. Numbers obtained from: 
# https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHWG/Higgs_XSBR_YR4_update.xlsx
# https://pdg.lbl.gov/2022/listings/contents_listings.html
mh         = 125.4                  # Observed H(125) mass
br_hgamgam = 2.27e-3                # BR(H(125)->gammagamma)
br_hbb     = 5.76e-1                # BR(H(125)->bb)
fb2pb      = 1e-3                   # Translation fb->pb

import csv
# Set up the model
import mssm_xs_tools 
mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/mh125EFT_13.root", True, 0)
def ggHhh(mA, tb): 
    return mssm.xsec(b"gg->H", mA, tb)*mssm.br(b"H->hh", mA, tb)
def mH2mA(mX, tb):
    return mssm.mass2mA(b"H", mX, tb)
# Set up the scan
start = 60
stop  = 0.5
step  =-0.5

def recast_limits(source, target, mass_column, limit_column, br_H1=1., br_H2=1., HHambiguity=2.): 
    # Read
    contour = []
    from mssm_extra_tools import mA_tanb_scan
    with open(source) as f:
        r=csv.DictReader(f, delimiter=",")
        for l in r:
            OBS_LIMIT=float(l[limit_column])/HHambiguity*fb2pb/br_H1/br_H2
            OBS_MASS=float(l[mass_column])
            contour.append(
                mA_tanb_scan(
                    OBS_LIMIT, 
                    OBS_MASS, 
                    mH2mA, 
                    ggHhh, 
                    start, 
                    stop, 
                    step
                    )
                )
    # Write
    with open(target, mode="w") as f:
        w=csv.writer(f, delimiter=",")
        w.writerow(["mA","tanb"])
        for l in contour:
            if not l[1]==stop:
                w.writerow(l)

if __name__=="__main__":
    # HIG-21-011 is a limit on BR(X->H(gamgam)H(bb))
    #recast_limits("./csv_files/HIG-21-011_obs.csv", "./csv_files/HIG-21-011_mAtanb_obs.csv", "mX", "limit", br_gamgam, br_bb)
    #recast_limits("./csv_files/HIG-21-011_exp.csv", "./csv_files/HIG-21-011_mAtanb_exp.csv", "mX", "limit", br_gamgam, br_bb)
    # HIG-21-005 is a limit on BR(X->HH)
    #recast_limits("./csv_files/HIG-21-005_obs.csv", "./csv_files/HIG-21-005_mAtanb_obs.csv", "mX", "limit")
    #recast_limits("./csv_files/HIG-21-005_exp.csv", "./csv_files/HIG-21-005_mAtanb_exp.csv", "mX", "limit")
    #recast_limits("./csv_files/B2G-23-002_obs.csv", "./csv_files/HIG-23-002_mAtanb_obs.csv", "mX", "limit")
    # B2G-23-002 HH combination --> a limit on BR(X->HH), HH ambiguity already taken into account upstream
    recast_limits("./csv_files/B2G-23-002_exp.csv", "./csv_files/B2G-23-002_mAtanb_exp.csv", "mX", "limit", HHambiguity=1.)

