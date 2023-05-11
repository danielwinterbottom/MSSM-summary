import csv
# Set up the model; The SM cross section for ttbar production at 13.6 TeV is 
# estimated with 921 pb
import mssm_xs_tools 
mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/mh125_13.root", True, 0)
def lowmass_Hptaunu(mHp, tb):
    return 2*921.*mssm.br(b"t->Hpb", mHp, tb)*mssm.br(b"Hp->taunu", mHp, tb)
def highmass_Hptaunu(mHp, tb): 
    return 2*mssm.xsec(b"pp->Hp", mHp, tb)*mssm.br(b"Hp->taunu", mHp, tb)
def mHp2mA(mHp, tb):
    return mssm.mass2mA(b"Hp", mHp, tb)
# Set up the scan
start = 0.5
stop  = 60.
step  = 0.5

def recast_limits(source, target, mass_column, limit_column): 
    # Read
    contour = []
    from mssm_extra_tools import mA_tanb_scan
    with open(source) as f:
        r=csv.DictReader(f, delimiter=",")
        for l in r:
            mHp = float(l[mass_column])
            if mHp<=180:
                contour.append(mA_tanb_scan(float(l[limit_column]), mHp, 
                mHp2mA, lowmass_Hptaunu, start, stop, step, lockmX=True))
            else:
                contour.append(mA_tanb_scan(float(l[limit_column]), mHp, 
                mHp2mA, highmass_Hptaunu, start, stop, step, lockmX=True))
    # Write
    with open(target, mode="w") as f:
        w=csv.writer(f, delimiter=",")
        w.writerow(["mA","tanb"])
        for l in contour:
            if not l[1]==stop:
                w.writerow(l)

if __name__=="__main__":
    recast_limits("./csv_files/HIG-18-014_obs.csv", "./csv_files/HIG-18-014_mAtanb_obs.csv", "mX", "limit")
    recast_limits("./csv_files/HIG-18-014_exp.csv", "./csv_files/HIG-18-014_mAtanb_exp.csv", "mX", "limit")
