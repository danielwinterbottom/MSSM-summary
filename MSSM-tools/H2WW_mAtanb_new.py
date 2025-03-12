import ROOT
import json
import numpy as np
from contour_tools import *

width_dep = False # note for HIG-20-016 width dependent limits only start at mH=300 GeV
br_2l2n    = (1.086e-1*3)**2 

reverse = False

def read_json_to_graph_old(json_file): #TODO delete
    masses = []
    widths = []
    limits = []

    with open(json_file, 'r') as f:
        data = json.load(f)
        for width in data:
            for mass in data[width]:
                masses.append(float(mass))
                if width == '0.1%': widths.append(0.) # for NWA set this to 0
                else: widths.append(float(width.replace('%',''))/100*float(mass))
                limits.append(data[width][mass]/br_2l2n) # need to factor out the WW branching fraction         

    graph = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(limits))
    return graph

def read_json_to_graphs_NWA_old(json_file): #TODO delete
    masses = []
    widths = []
    observed = []
    expected = []

    with open(json_file, 'r') as f:
        data = json.load(f)
        # if not using width dependent limits we take the width as 0 (= NWA)
        for mass in data:
            masses.append(float(mass))
            widths.append(0.)
            observed.append(data[mass]['obs']/br_2l2n) # need to factor out the WW branching fraction         
            expected.append(data[mass]['exp0']/br_2l2n) # need to factor out the WW branching fraction         
            # duplicate points for 100% width so interpolation will always return same values independent of the widths
            masses.append(masses[-1])
            widths.append(masses[-1]) # i.e a 100% width
            observed.append(observed[-1])
            expected.append(expected[-1])


    graph_exp = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(expected))
    graph_exp.SetName('g_exp')
    graph_obs = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(observed))
    graph_obs.SetName('g_obs')

    return graph_obs, graph_exp


if __name__ == "__main__":

    benchmark = "mh125EFT"

    proc = 'gg'
    print (f"Processing {benchmark} with {proc}H production")

    if width_dep:

        if proc == 'gg': 
            limits_file_exp = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_ggH_exp0.json"
            limits_file_obs = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_ggH_obs.json"
        elif proc == 'vbf': 
            limits_file_exp = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_VBF_exp0.json"
            limits_file_obs = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_VBF_obs.json"
        else:
            # else we are defining limits for the sum of VBF and ggH so we taking floating fVBF limits
            limits_file_exp = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_float_exp0.json"
            limits_file_obs = "MSSM-tools/json_files/HtoWWto2L2NuRun2/2DWidthOutput_float_obs.json"

        print(f"Using limits from {limits_file_exp} and {limits_file_obs}")

        g_exp = read_json_to_graph(limits_file_exp)
        g_exp.SetName('g_exp')
        g_obs = read_json_to_graph(limits_file_obs)
        g_obs.SetName('g_obs')

    else:
        if proc == 'gg':
            limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_ggH.json'
        elif proc == 'vbf':
            limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_VBF.json'
        else: 
            limits_file = 'MSSM-tools/json_files/HtoWWto2L2NuRun2/indep_float.json'

        print(f"Using limits from {limits_file}")

        g_obs, g_exp = read_json_to_graphs_NWA(limits_file)

    mssm_bm_file = f"MSSM-tools/root_files/{benchmark}_13.root"

    f = ROOT.TFile(mssm_bm_file)

    h_H_mass = f.Get('m_H')
    h_H_width = f.Get('width_H')

    if proc in ['gg','vbf']: h_xs = f.Get(f'xs_{proc}_H')
    else: 
        h_xs = f.Get(f'xs_gg_H')
        h_xs.Add(f.Get(f'xs_vbf_H'))

    h_BR_HWW = f.Get('br_H_WW')

    # find the smallest mass in the limits
    min_mass = 10000
    for p in range(g_exp.GetN()):
        mass = g_exp.GetX()[p]
        if mass < min_mass:
            min_mass = mass

    print(f"Minimum mass in the limits is {min_mass}")


    g_excluded_exp = ROOT.TGraph()
    g_excluded_exp.SetName('g_excluded_exp')
    g_excluded_obs = ROOT.TGraph()
    g_excluded_obs.SetName('g_excluded_obs')

    h_excluded_exp = ROOT.TH2D('h_excluded_exp','',1000,85,1000,1000,h_H_mass.GetYaxis().GetBinLowEdge(1),h_H_mass.GetYaxis().GetBinUpEdge(h_H_mass.GetNbinsY()))
    h_excluded_obs = ROOT.TH2D('h_excluded_obs','',1000,85,1000,1000,h_H_mass.GetYaxis().GetBinLowEdge(1),h_H_mass.GetYaxis().GetBinUpEdge(h_H_mass.GetNbinsY()))

    for y in range(1,h_excluded_exp.GetNbinsY()+1):
        for x in range(1,h_excluded_exp.GetNbinsX()+1):
            tanb = h_excluded_exp.GetYaxis().GetBinCenter(y)
            mA   = h_excluded_exp.GetXaxis().GetBinCenter(x)

            mH = h_H_mass.Interpolate(mA, tanb)
            width = h_H_width.Interpolate(mA, tanb)

            xs = h_xs.Interpolate(mA, tanb)
            br = h_BR_HWW.Interpolate(mA, tanb)*br_2l2n # multiple by the WW->2L2Nu branching fraction

            obs = g_obs.Interpolate(mH, width)
            exp = g_exp.Interpolate(mH, width)

            # check if xs*br is excluded (less than exp/obs limits)
            #if it is excluded add a point to g_excluded_exp and g_excluded_obs

            bini = h_excluded_exp.FindBin(mA,tanb)
            if xs*br > exp and mH > min_mass and mA <1000: # maybe change this to 500?
                g_excluded_exp.SetPoint(g_excluded_exp.GetN(), mA, tanb)
            if xs*br > obs and mH > min_mass and mA<1000:
                g_excluded_obs.SetPoint(g_excluded_obs.GetN(), mA, tanb)

            if reverse:
                r_exp = 0. if exp <=0 else (xs*br)/exp
                r_obs = 0. if obs <= 0 else (xs*br)/obs
            else:
                r_exp = 0. if (xs*br) <=0 else exp/(xs*br)
                r_obs = 0. if (xs*br) <= 0 else obs/(xs*br)
            h_excluded_exp.SetBinContent(x,y, r_exp)
            h_excluded_obs.SetBinContent(x,y, r_obs)

if proc not in ['gg','vbf']: proc = 'all'

fout = ROOT.TFile(f'{benchmark}_HWW_graphs_{proc}.root', 'recreate')
g_excluded_obs.Write()
g_excluded_exp.Write()
h_excluded_obs.Write()
h_excluded_exp.Write()

# get a graph corresponding the to maximum values of the excluded region
g_excluded_exp_max = ROOT.TGraph()
g_excluded_exp_max.SetName('g_excluded_exp_max')
g_excluded_obs_max = ROOT.TGraph()
g_excluded_obs_max.SetName('g_excluded_obs_max')

max_map = {}

for p in range(g_excluded_exp.GetN()):
    mA = g_excluded_exp.GetX()[p]
    if mA not in max_map:
        max_map[mA] = g_excluded_exp.GetY()[p]
    elif g_excluded_exp.GetY()[p] > max_map[mA]:
        max_map[mA] = g_excluded_exp.GetY()[p]

for i, mA in enumerate(max_map):
    # skip points to reduce the number of points in the graph
    g_excluded_exp_max.SetPoint(g_excluded_exp_max.GetN(), mA, max_map[mA])

max_map = {}

for p in range(g_excluded_obs.GetN()):
    mA = g_excluded_obs.GetX()[p]
    if mA not in max_map:
        max_map[mA] = g_excluded_obs.GetY()[p]
    elif g_excluded_obs.GetY()[p] > max_map[mA]:
        max_map[mA] = g_excluded_obs.GetY()[p]

for mA in max_map:
    g_excluded_obs_max.SetPoint(g_excluded_obs_max.GetN(), mA, max_map[mA])

g_excluded_exp_max.Write()
g_excluded_obs_max.Write()


# get countours from 2H histograms instead
contours_obs = contourFromTH2(h_excluded_obs,1.)
contours_exp = contourFromTH2(h_excluded_exp,1.)

def CombineContours(contours):
    """
    Combine contours into 1 TGraph so they can be drawn  as a filled area
    """

    filled_region = ROOT.TGraph()

    for i in range(contours[0].GetN()):
        filled_region.SetPoint(i, contours[0].GetX()[i], contours[0].GetY()[i])
    for N, c in enumerate(contours[1:]):
        for i in range(c.GetN()):
            filled_region.SetPoint(filled_region.GetN(),
                                   c.GetX()[c.GetN() - 1 - i],
                                   c.GetY()[c.GetN() - 1 - i])
        filled_region.SetPoint(filled_region.GetN(),
                     contours[0].GetX()[contours[0].GetN() - 1],
                     contours[0].GetY()[contours[0].GetN() - 1])
    
    return filled_region

if reverse:
    max_points = 0
    max_graph = None
    for graph in contours_obs:
        if graph.GetN() > max_points:
            max_points = graph.GetN()
            max_graph = graph
    
    max_graph.Write('contour0_obs')
    
    max_points = 0
    max_graph = None
    for graph in contours_exp:
        if graph.GetN() > max_points:
            max_points = graph.GetN()
            max_graph = graph
    max_graph.Write('contour0_exp')

else:
    contours_obs[0].Write('contour0_obs')
    contours_exp[0].Write('contour0_exp')

contour_cmb_obs = CombineContours(contours_obs)
contour_cmb_exp = CombineContours(contours_exp)

contour_cmb_obs.Write('contour_cmb_obs')
contour_cmb_exp.Write('contour_cmb_exp')
