# This script converts limits on cross-sections to limits on the mAtanb plane for a given benchmark scenario
# Currently WW, ZZ and hh decay modes are supported

#Latest commands used for results in summary plot (13/03/25)
#H->WW: for bm in mh125EFT mh125 hMSSM; do python3 MSSM-tools/Get_mAtanb_regions.py --decay WW --benchmark ${bm}; done
#H->ZZ: for bm in mh125EFT mh125 hMSSM; do python3 MSSM-tools/Get_mAtanb_regions.py --decay ZZ --benchmark ${bm}; done


import ROOT
import json
import numpy as np
from contour_tools import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--proc', type=str, default='gg', help='Production mode (gg, vbf, bb, gg+bb, gg+vbf, all)')
parser.add_argument('--decay', type=str, help='Decay mode (WW, ZZ, hh)')
parser.add_argument('--higgs', type=str, default='H', help='Higgs boson to consider: H or A')
parser.add_argument('--benchmark', type=str, default='mh125EFT', help='Benchmark scenario')

args = parser.parse_args()

if args.proc not in ['gg','vbf','bb','gg+bb','gg+vbf','all']: 
    print(f"Invalid production mode {args.proc}. Supported modes are gg, vbf, bb, gg+bb, gg+vbf, all")
    exit(1)
if args.decay not in ['WW','ZZ','hh']:
    print(f"Invalid decay mode {args.decay}. Supported modes are WW, ZZ, hh")
    exit(1)
if args.higgs not in ['H','A']:
    print(f"Invalid Higgs boson {args.higgs}. Supported bosons are H, A")
    exit(1)

print (f"Processing {args.benchmark} with {args.proc} {args.higgs} production and {args.higgs}->{args.decay} decay")

#for now we hardcode the locations of the json/csv files and whether the width dependent limits are taken, but these could be added as options in the future

br_extra = 1. # If the limits include an additional branching ratio e.g WW->2L2Nu then we will need to scale the model xs*br by this number later on

if args.decay == 'WW':
    
    if args.proc == 'gg':
        # this assumed 100% gg i.e no VBF
        limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_ggH.json'
    elif args.proc == 'vbf':
        # this assumed 100% VBF i.e no ggH
        limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_VBF.json'
    else: 
        # any other option for proc takes the most general limits but note this may not be accurate in all cases e.g if bb production is large 
        limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_float.json'
    
    br_extra = (1.086e-1*3)**2 #The WW->2L2Nu branching ratio
   
    g_obs, g_exp = read_json_to_graphs_NWA(limits_file)

if args.decay == 'ZZ':

    # we use width dependent limits for ZZ decay
    # note that the limits specified below may not always be accurate e.g if bb production is large
    if args.proc == 'vbf': 
        limits_file = "MSSM-tools/csv_files/HtoZZto4LRun2/VBF_2D_Run2.csv"
    else: 
        limits_file = "MSSM-tools/csv_files/HtoZZto4LRun2/ggF_2D_Run2.csv"

    g_obs, g_exp = read_csv_to_graphs(limits_file)

if args.decay == 'hh':
    limits_file = "MSSM-tools/json_files/GGF_Radion_HH_B2G-23-002.json"

    g_obs, g_exp = read_json_to_graphs_NWA(limits_file, obs_name='observed', exp_name='limit', units='fb')

print(f"Using limits from {limits_file}") 

# get MSSM benchmark file
mssm_bm_file = f"MSSM-tools/root_files/{args.benchmark}_13.root"
f = ROOT.TFile(mssm_bm_file)

# get histogram of cross-sections vs mA and tanb
if args.proc in ['gg','vbf','bb']: h_xs = f.Get(f'xs_{args.proc}_{args.higgs}')
elif args.proc == 'gg+bb':
    h_xs = f.Get(f'xs_gg_{args.higgs}')
    h_xs.Add(f.Get(f'xs_bb_{args.higgs}'))
elif args.proc == 'gg+vbf':
    h_xs = f.Get(f'xs_gg_{args.higgs}')
    h_xs.Add(f.Get(f'xs_vbf_{args.higgs}'))
elif args.proc == 'all':
    h_xs = f.Get(f'xs_gg_{args.higgs}')
    h_xs.Add(f.Get(f'xs_bb_{args.higgs}'))
    h_xs.Add(f.Get(f'xs_vbf_{args.higgs}'))

# get histogram of branching ratios vs mA and tanb
h_br = f.Get(f'br_{args.higgs}_{args.decay}')

# get histograms of Higgs mass and width vs mA and tanb
h_mass = f.Get(f'm_{args.higgs}')
h_width = f.Get(f'width_{args.higgs}')
h_hmass = f.Get('m_h')

# find the smallest mass in the limits
min_mass = 10000
for p in range(g_exp.GetN()):
    mass = g_exp.GetX()[p]
    if mass < min_mass:
        min_mass = mass
print(f"Minimum mass in the limits is {min_mass}")


# currently hardcode mA range but this could be made an option in the future
mA_range = (85,1000)

h_excluded_exp = ROOT.TH2D('h_exp','',1000,mA_range[0],mA_range[1],1000,h_mass.GetYaxis().GetBinLowEdge(1),h_mass.GetYaxis().GetBinUpEdge(h_mass.GetNbinsY()))
h_excluded_obs = ROOT.TH2D('h_obs','',1000,mA_range[0],mA_range[1],1000,h_mass.GetYaxis().GetBinLowEdge(1),h_mass.GetYaxis().GetBinUpEdge(h_mass.GetNbinsY()))

for y in range(1,h_excluded_exp.GetNbinsY()+1):
    for x in range(1,h_excluded_exp.GetNbinsX()+1):

        tanb = h_excluded_exp.GetYaxis().GetBinCenter(y)
        mA   = h_excluded_exp.GetXaxis().GetBinCenter(x)

        if args.higgs == 'H':
            mX = h_mass.Interpolate(mA, tanb)
        else:
            mX = mA

        width = h_width.Interpolate(mA, tanb)
        xs = h_xs.Interpolate(mA, tanb)
        br = h_br.Interpolate(mA, tanb)*br_extra # multiple by the extra branching fraction
        obs = g_obs.Interpolate(mX, width)
        exp = g_exp.Interpolate(mX, width)

        # now we store a histogram of the limit divide by the XS*BR so all values < 1 are excluded
        r_exp = 100000. if mX<min_mass or (xs*br) <=0 else exp/(xs*br) # set large values if mass value is out of the explored range or if the predicted XS*BR is zero (i.e so it is not excluded)
        r_obs = 100000. if mX<min_mass or (xs*br) <=0 else obs/(xs*br)

        h_excluded_exp.SetBinContent(x,y, r_exp)
        h_excluded_obs.SetBinContent(x,y, r_obs)

fout = ROOT.TFile(f'{args.benchmark}_{args.proc}To{args.higgs}To{args.decay}_mAtanb_contours.root', 'recreate')

h_excluded_obs.Write()
h_excluded_exp.Write()

# get countours from 2D histograms 
contours_obs = contourFromTH2(h_excluded_obs,1.)
contours_exp = contourFromTH2(h_excluded_exp,1.)

# store integer indicating the number of contours on the output file
n_contours = len(contours_obs)
fout.WriteObject(ROOT.TParameter("int")("n_contours", n_contours), 'n_contours')

# sort countours them by the number of points in the graphs (largest first)
contours_obs = sorted(contours_obs, key=lambda x: x.GetN(), reverse=True)
contours_exp = sorted(contours_exp, key=lambda x: x.GetN(), reverse=True)

# now write all contours to the output file
for i, c in enumerate(contours_obs):
    c.Write(f'contour_obs_{i}')
for i, c in enumerate(contours_exp):
    c.Write(f'contour_exp_{i}')

contour_cmb_obs = CombineContours(contours_obs)
contour_cmb_exp = CombineContours(contours_exp)

contour_cmb_obs.Write('contour_cmb_obs')
contour_cmb_exp.Write('contour_cmb_exp')

def HistExcludedPoints(hist):
    """
    make a histogram where only the points excluded are shown
    excluded points have value=1 and non-excluded points have value=0
    """

    h = hist.Clone()
    h.Reset()
    h.SetName(h.GetName()+'_excluded')
    for y in range(1,h.GetNbinsY()+1):
        for x in range(1,h.GetNbinsX()+1):
            if hist.GetBinContent(x,y) < 1:
                h.SetBinContent(x,y,1)
    return h

h_excluded_obs_points = HistExcludedPoints(h_excluded_obs)
h_excluded_exp_points = HistExcludedPoints(h_excluded_exp)

#Write to output:
h_excluded_obs_points.Write('h_obs_excluded')
h_excluded_exp_points.Write('h_exp_excluded')
