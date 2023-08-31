"""
Tanslate exclusion contours from mA tanb in a given model into xsec*BR limits.

These can be picked up as pseudo-limits to translate them back into other
models. This strategy only works if the exclusion contour is driven by a single
production mode.
"""
import csv
# Set up the model
import mssm_xs_tools 
mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/hMSSM_13.root", True, 0)

def xsec(mA, tb): 
    return mssm.xsec("gg->H", mA, tb)*mssm.br("H->WW", mA, tb)
def mass(mA, tb, type="H"):
    return mssm.mass(type, mA, tb)

limit=[]
def model2xsec(source, target, mA_column="mA", tb_column="tanb"):
    with open(source, "r") as f:
        d=csv.DictReader(f, delimiter=",")
        for l in d:
            mA=float(l[mA_column])
            tb=float(l[tb_column])
            limit.append((mass(mA, tb, "H"), xsec(mA, tb)))
    with open(target, "w") as f:
        w=csv.writer(f)
        w.writerow("mX,limit".split(","))
        for l in limit:
            w.writerow(["{}".format(i) for i in l])

if __name__=="__main__":
    model2xsec("./csv_files/HIG-17-033_mAtanb_hMSSM_obs.csv", "./csv_files/HIG-17-033_obs_extrap_hMSSM.csv")
    model2xsec("./csv_files/HIG-17-033_mAtanb_hMSSM_exp.csv", "./csv_files/HIG-17-033_exp_extrap_hMSSM.csv")
