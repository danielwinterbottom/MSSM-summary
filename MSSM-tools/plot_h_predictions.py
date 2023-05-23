#import pandas as pd
#import numpy as np

import mssm_xs_tools 
from mssm_extra_tools import scale2mobs as scale

import ROOT 
ROOT.gStyle.SetOptStat(0)

# ------------------------------------------------------------------------------
# SM prediction
# 
SM_xs = {
    "ggH" : 4.830E+01,
    }
SM_br = {
    "gamgam" : 2.270E-03,
    "ZZ"     : 2.716E-02,
    "WW"     : 2.203E-01,
    "tautau" : 6.208E-02,
    }

# ------------------------------------------------------------------------------
# Limits
#
# obtained from:
# HIG-17-031: http://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-17-031/CMS-HIG-17-031_Table_003.pdf
#               lower|upper
Limit_HIG_17_031_exp = {
    "gamgam" : (0.68, 1.34),
    "ZZ"     : (0.60, 1.44),
    "WW"     : (0.68, 1.34),
    "tautau" : (0.18, 1.90),
}
#               lower|upper
Limit_HIG_17_031_obs = {
    "gamgam" : (0.80, 1.58),
    "ZZ"     : (0.80, 1.68),
    "WW"     : (0.97, 1.77),
    "tautau" : (0.11, 2.11),
}
# HIG-22-001: http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2021_214_v9.pdf (Table 13)
#               lower|upper
Limit_HIG_22_001_exp = {
    "gamgam" : (0.78, 1.22),
    "ZZ"     : (0.74, 1.28),
    "WW"     : (0.78, 1.22),
    "tautau" : (0.54, 1.50),
}
#               lower|upper
Limit_HIG_22_001_obs = {
    "gamgam" : (0.86, 1.32),
    "ZZ"     : (0.67, 1.21),
    "WW"     : (0.70, 1.12),
    "tautau" : (0.20, 1.16),    
}

def fill_data(limit_exp, limit_obs, model, chn):
    # Define the grid to work with
    mA = list(range(130, 1000, 10))
    tb = list(range(  1,   60,  1))
    
    # Define BSM model
    mssm = mssm_xs_tools.mssm_xs_tools(model, True, 0)
    pred = lambda mA,tb : scale(mssm.mass(b"h", mA, tb), "ggH", chn)*mssm.xsec(b"gg->h", mA, tb)*mssm.br(b"h->{}".format(chn), mA, tb)

    # Define TH2F historgrams
    hmod = ROOT.TH2F("hmod", "", len(mA), mA[0], mA[-1], len(tb), tb[0], tb[-1])
    hexp = ROOT.TH2F("hexp", "", len(mA), mA[0], mA[-1], len(tb), tb[0], tb[-1])
    hobs = ROOT.TH2F("hobs", "", len(mA), mA[0], mA[-1], len(tb), tb[0], tb[-1])

    #plane = []
    for t in tb:
        print("Filling data for tanb=", t)
        #plane.append([pred(i,t)/SM_xs/SM_br for i in mA])
        for i in mA:
            p=pred(i,t)/SM_xs["ggH"]/SM_br[chn]
            #print(i, t, p)    
            hmod.Fill(i, t, p)
            if p<limit_exp[0] or p>limit_exp[1]:
                hexp.Fill(i, t, 10)
            if p<limit_obs[0] or p>limit_obs[1]:
                hobs.Fill(i, t, 10)
    #model = pd.DataFrame(plane, columns=mA)
    #print(model)
    return hmod, hexp, hobs

def plot_data(limit_exp, limit_obs, model="hMSSM", chn="gamgam", label="HIG_17_031"):
    canv = ROOT.TCanvas("canv", "Model/SM", 600, 600)
    hmod, hexp, hobs = fill_data(limit_exp, limit_obs, model=b"root_files/{model}_13.root".format(model=model), chn=chn)
    hmod.Draw("colz")
    hexp.SetMarkerColor(kBlue)
    hexp.Draw("same")
    hobs.SetMarkerColor(kMagenta)
    hobs.Draw("same")
    canv.Print("hmodel_{model}_{chn}_{label}.pdf".format(model=model, chn=chn, label=label))

if __name__=="__main__":
    dataset_exp = {
        "HIG_17_031"  : Limit_HIG_17_031_exp,
        "HIG_22_001"  : Limit_HIG_22_001_exp,
        }
    dataset_obs = {
        "HIG_17_031"  : Limit_HIG_17_031_obs,
        "HIG_22_001"  : Limit_HIG_22_001_obs,
        }
    for chn in ["gamgam", "ZZ", "WW", "tautau"]:
        for model in ["hMSSM", "mh125"]:
            for ds in ["HIG_17_031", "HIG_22_001"]:
                print("Plotting limits for h->{chn}, {model}, {dataset}".format(chn=chn, model=model, dataset=ds))
                plot_data(dataset_exp[ds][chn], dataset_obs[ds][chn], model=model, chn=chn, label=ds)
