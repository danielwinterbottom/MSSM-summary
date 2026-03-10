import ROOT
import json
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../MSSM-tools")
from contour_tools import *
import argparse
from SingletXSBRs import SingletXSBRs

# note CMS h125 inclusive signal strength measurment = 1.01 ± 0.05

parser = argparse.ArgumentParser()
parser.add_argument('--proc', type=str, default='gg', help='Production mode (gg, vbf, bb, gg+bb, gg+vbf, all)')
parser.add_argument('--decay', type=str, help='Decay mode (WW, ZZ, hh)')
parser.add_argument('--tanb', type=float, default=1.0, help='The value of tan(beta)')

args = parser.parse_args()

if args.proc not in ['gg','vbf','gg+vbf']: 
    print(f"Invalid production mode {args.proc}. Supported modes are gg, vbf, bb, gg+bb, gg+vbf, all")
    exit(1)
if args.decay not in ['WW','ZZ','hh']:
    print(f"Invalid decay mode {args.decay}. Supported modes are WW, ZZ, hh")
    exit(1)

print (f"Processing limits for tanb={args.tanb} with {args.proc} H production and H->{args.decay} decay")    

br_extra = 1. # If the limits include an additional branching ratio e.g WW->2L2Nu then we will need to scale the model xs*br by this number later on

if args.decay == 'WW':
    
    if args.proc == 'gg':
        # this assumed 100% gg i.e no VBF
        limits_file = '../MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_ggH.json'
    elif args.proc == 'vbf':
        # this assumed 100% VBF i.e no ggH
        limits_file = '../MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_VBF.json'
    else: 
        # for other production modes we take the SM-like ggH and VBF fractions  
        limits_file = '../MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_SM.json'
    
    br_extra = (1.086e-1*3)**2 #The WW->2L2Nu branching ratio
   
    g_obs, g_exp = read_json_to_graphs_NWA(limits_file)

if args.decay == 'ZZ':

    # we use width dependent limits for ZZ decay
    # note that the limits specified below may not always be accurate e.g if bb production is large
    if args.proc == 'vbf': 
        limits_file = "../MSSM-tools/csv_files/HtoZZto4LRun2/VBF_2D_Run2.csv"
    else: 
        limits_file = "../MSSM-tools/csv_files/HtoZZto4LRun2/ggF_2D_Run2.csv"

    g_obs, g_exp = read_csv_to_graphs(limits_file,mass_column=0,width_column=1, obs_column=2, exp_column=5)
#obs_column=2, exp_column=3
if args.decay == 'hh':
    limits_file = "../MSSM-tools/json_files/GGF_Radion_HH_B2G-23-002.json"

    g_obs, g_exp = read_json_to_graphs_NWA(limits_file, obs_name='observed', exp_name='limit', units='fb')

print(f"Using limits from {limits_file}") 

# find the smallest mass in the limits
min_mass = 10000
for p in range(g_exp.GetN()):
    mass = g_exp.GetX()[p]
    if mass < min_mass:
        min_mass = mass
print(f"Minimum mass in the limits is {min_mass}")

# currently hardcode sina-mH range but this could be made an option in the future
mH_range = (125,1000)
sina_range = (-0.5,0.5)

h_excluded_exp = ROOT.TH2D('h_exp','',1000,mH_range[0],mH_range[1],1000,sina_range[0],sina_range[1])
h_excluded_obs = ROOT.TH2D('h_obs','',1000,mH_range[0],mH_range[1],1000,sina_range[0],sina_range[1])

xsbr_tool = SingletXSBRs() # tool for evaluating the XS, BRs, and widths

for y in range(1,h_excluded_exp.GetNbinsY()+1):
    for x in range(1,h_excluded_exp.GetNbinsX()+1):

        sina = h_excluded_exp.GetYaxis().GetBinCenter(y)
        mH   = h_excluded_exp.GetXaxis().GetBinCenter(x)

        width = xsbr_tool.ComputeWidth(mH, args.tanb, sina)
        if width/mH>0.1 and mH>130 and sina>-0.35 and sina<0.35: print(sina, mH, width, width/mH)

        obs = g_obs.Interpolate(mH, width)
        exp = g_exp.Interpolate(mH, width)

        if args.proc in ['gg','vbf']: 
            xsbr = xsbr_tool.ComputeXSBR(mH, args.tanb, sina, args.proc, args.decay)
        else:
            xsbr = xsbr_tool.ComputeXSBR(mH, args.tanb, sina, 'gg', args.decay)
            xsbr += xsbr_tool.ComputeXSBR(mH, args.tanb, sina, 'vbf', args.decay)
        xsbr*=br_extra

        # now we store a histogram of the limit divide by the XS*BR so all values < 1 are excluded
        r_exp = 100000. if mH<min_mass or xsbr <=0 else exp/xsbr # set large values if mass value is out of the explored range or if the predicted XS*BR is zero (i.e so it is not excluded)
        r_obs = 100000. if mH<min_mass or xsbr <=0 else obs/xsbr

        h_excluded_exp.SetBinContent(x,y, r_exp)
        h_excluded_obs.SetBinContent(x,y, r_obs)

benchmark_name = f'singlet_tanb{args.tanb}'.replace('.','p')

fout = ROOT.TFile(f'{benchmark_name}_{args.proc}ToHTo{args.decay}_mHsina_contours.root', 'recreate')

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