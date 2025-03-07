import ROOT
import csv
import numpy as np

def read_csv_to_graphs(file_path):
    masses = []
    widths = []
    observed = []
    expected = []
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for row in reader:
            mass = float(row[0])
            width = float(row[1])
            obs = float(row[2])
            exp = float(row[5])
            
            masses.append(mass)
            widths.append(width)
            observed.append(obs)
            expected.append(exp)
    
    graph_obs = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(observed))
    graph_obs.SetName('g_obs')
    graph_exp = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(expected))
    graph_exp.SetName('g_exp')

    return graph_obs, graph_exp



if __name__ == "__main__":

    benchmark = "mh125EFT"

    proc = 'vbf'

    if proc == 'gg': limits_file = "MSSM-tools/csv_files/HtoZZto4LRun2/ggF_2D_Run2.csv"
    else: limits_file = "MSSM-tools/csv_files/HtoZZto4LRun2/VBF_2D_Run2.csv"

    print (f"Processing {benchmark} with {proc}H production")
    print(f"Using limits from {limits_file}")

    mssm_bm_file = f"MSSM-tools/root_files/{benchmark}_13.root"

    f = ROOT.TFile(mssm_bm_file)

    h_H_mass = f.Get('m_H')
    h_H_width = f.Get('width_H')
    h_xs_ggH = f.Get(f'xs_{proc}_H')
    h_BR_HZZ = f.Get('br_H_ZZ')

    g_obs, g_exp = read_csv_to_graphs(limits_file)

    tanb_step = 0.1
    mA_step = 1

    g_excluded_exp = ROOT.TGraph()
    g_excluded_exp.SetName('g_excluded_exp')
    g_excluded_obs = ROOT.TGraph()
    g_excluded_obs.SetName('g_excluded_obs')


    for tanb in np.arange(h_H_mass.GetYaxis().GetBinLowEdge(1), h_H_mass.GetYaxis().GetBinUpEdge(h_H_mass.GetNbinsY()), tanb_step):
        for mA in np.arange(h_H_mass.GetXaxis().GetBinLowEdge(1), h_H_mass.GetXaxis().GetBinUpEdge(h_H_mass.GetNbinsX()), mA_step):

            #print(mA,tanb)
            mH = h_H_mass.Interpolate(mA, tanb)
            width = h_H_width.Interpolate(mA, tanb)

            xs = h_xs_ggH.Interpolate(mA, tanb)
            br = h_BR_HZZ.Interpolate(mA, tanb)

            obs = g_obs.Interpolate(mH, width)
            exp = g_exp.Interpolate(mH, width)

            # check if xs*br is excluded (less than exp/obs limits)
            #if it is excluded add a point to g_excluded_exp and g_excluded_obs
            if xs*br > exp and mH > 130 and mA <500:
                g_excluded_exp.SetPoint(g_excluded_exp.GetN(), mA, tanb)

            if xs*br > obs and mH > 130 and mA<500:
                g_excluded_obs.SetPoint(g_excluded_obs.GetN(), mA, tanb)

fout = ROOT.TFile(f'{benchmark}_HZZ_graphs_{proc}.root', 'recreate')
g_excluded_obs.Write()
g_excluded_exp.Write()

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
    if i%5 != 0:
        continue
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




    


