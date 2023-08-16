# Inputs used for this recast. Numbers obtained from: 
# https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHWG/Higgs_XSBR_YR4_update.xlsx
# https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-18-005/CMS-HIG-18-005_Figure_005-a.png
br_hbb     = 5.76e-1                # BR(H(125)->bb)
br_htautau = 6.208e-2               # BR(H(125)->tautau)
br_Zll     = 6.73e-2                # BR(Z->ll)

import csv
# Set up the model
import mssm_xs_tools 
mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/mh125EFT_13.root", True, 0)
def ggAZh(mA, tb): 
    return mssm.xsec(b"gg->A", mA, tb)*mssm.br(b"A->Zh", mA, tb)
def mH2mA(mX, tb):
    return mssm.mass2mA(b"A", mX, tb)
# Set up the scan
start = 60
stop  = 0.5
step  =-0.5

def recast_limits(source, target, mass_column, limit_column, br_h=1., br_Z=1.): 
    # Read
    contour = []
    from mssm_extra_tools import mA_tanb_scan
    with open(source) as f:
        r=csv.DictReader(f, delimiter=",")
        for l in r:
            OBS_LIMIT=float(l[limit_column])/br_h/br_Z
            OBS_MASS=float(l[mass_column])
            contour.append(
                mA_tanb_scan(
                    OBS_LIMIT, 
                    OBS_MASS, 
                    mH2mA, 
                    ggAZh, 
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
    # HIG-18-005 is a limit on BR(A->ZH(bb))
    #recast_limits("./csv_files/HIG-18-005_exp.csv", "./csv_files/HIG-18-005_mAtanb_exp.csv", "mX", "limit", br_h=br_hbb)
    #recast_limits("./csv_files/HIG-18-005_obs.csv", "./csv_files/HIG-18-005_mAtanb_obs.csv", "mX", "limit", br_h=br_hbb)
    # HIG-18-023 is a limit in BR(A->Z(ll)H(tautau))
    recast_limits("./csv_files/HIG-18-023_exp.csv", "./csv_files/HIG-18-023_mAtanb_exp.csv", "mX", "limit", br_h=br_htautau, br_Z=br_Zll*1000.)
    recast_limits("./csv_files/HIG-18-023_obs.csv", "./csv_files/HIG-18-023_mAtanb_obs.csv", "mX", "limit", br_h=br_htautau, br_Z=br_Zll*1000.)

