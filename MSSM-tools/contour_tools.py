import ROOT
from array import array
import json
import csv
import numpy as np

ROOT.gROOT.SetBatch(1)

def contourFromTH2(h2in, threshold, minPoints=10, frameValue=1000.):
    # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html
    contoursList = [threshold]
    contours = array('d', contoursList)
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

    h2 = frameTH2D(h2in, threshold, frameValue)

    h2.SetContour(1, contours)

    # Draw contours as filled regions, and Save points
    # backup = ROOT.gPad # doesn't work in pyroot, backup behaves like a ref to gPad
    canv = ROOT.TCanvas('tmp', 'tmp')
    canv.cd()
    h2.Draw('CONT Z LIST')
    ROOT.gPad.Update()  # Needed to force the plotting and retrieve the contours in

    conts = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
    contLevel = None

    if conts is None or conts.GetSize() == 0:
        print('*** No Contours Were Extracted!')
        return None
    ret = ROOT.TList()
    for i in range(conts.GetSize()):
        contLevel = conts.At(i)
        print('>> Contour %d has %d Graphs' % (i, contLevel.GetSize()))
        for j in range(contLevel.GetSize()):
            gr1 = contLevel.At(j)
            print('\t Graph %d has %d points' % (j, gr1.GetN()))
            if gr1.GetN() > minPoints:
                ret.Add(gr1.Clone())
            # // break;
    # backup.cd()
    canv.Close()
    return ret

def frameTH2D(hist, threshold, frameValue=1000):
    # Now supports variable-binned histograms First adds a narrow frame (1% of
    # of bin widths) around the outside with same values as the real edge. Then
    # adds another frame another frame around this one filled with some chosen
    # value that will make the contours close

    # Get lists of the bin edges
    x_bins = [hist.GetXaxis().GetBinLowEdge(x)
              for x in range(1, hist.GetNbinsX() + 2)]
    y_bins = [hist.GetYaxis().GetBinLowEdge(y)
              for y in range(1, hist.GetNbinsY() + 2)]

    # New bin edge arrays will need an extra four values
    x_new = [0.] * (len(x_bins) + 4)
    y_new = [0.] * (len(y_bins) + 4)

    # Calculate bin widths at the edges
    xw1 = x_bins[1] - x_bins[0]
    xw2 = x_bins[-1] - x_bins[-2]
    yw1 = y_bins[1] - y_bins[0]
    yw2 = y_bins[-1] - y_bins[-2]

    # Set the edges of the outer framing bins and the adjusted
    # edge of the real edge bins
    x_new[0] = x_bins[0] - 2 * xw1 * 0.02
    x_new[1] = x_bins[0] - 1 * xw1 * 0.02
    x_new[-1] = x_bins[-1] + 2 * xw2 * 0.02
    x_new[-2] = x_bins[-1] + 1 * xw2 * 0.02
    y_new[0] = y_bins[0] - 2 * yw1 * 0.02
    y_new[1] = y_bins[0] - 1 * yw1 * 0.02
    y_new[-1] = y_bins[-1] + 2 * yw2 * 0.02
    y_new[-2] = y_bins[-1] + 1 * yw2 * 0.02

    # Copy the remaining bin edges from the hist
    for i in range(0, len(x_bins)):
        x_new[i + 2] = x_bins[i]
    for i in range(0, len(y_bins)):
        y_new[i + 2] = y_bins[i]

    # print x_new
    # print y_new

    framed = ROOT.TH2D('%s framed' % hist.GetName(), '%s framed' % hist.GetTitle(), len(
        x_new) - 1, array('d', x_new), len(y_new) - 1, array('d', y_new))
    framed.SetDirectory(0)

    for x in range(1, framed.GetNbinsX() + 1):
        for y in range(1, framed.GetNbinsY() + 1):
            if x == 1 or x == framed.GetNbinsX() or y == 1 or y == framed.GetNbinsY():
        # This is a a frame bin
                framed.SetBinContent(x, y, frameValue)
            else:
                # adjust x and y if we're in the first frame so as to copy the output
                # values from the real TH2
                ux = x
                uy = y
                if x == 2:
                    ux += 1
                elif x == (len(x_new) - 2):
                    ux -= 1
                if y == 2:
                    uy += 1
                elif y == (len(y_new) - 2):
                    uy -= 1
                framed.SetBinContent(x, y, hist.GetBinContent(ux - 2, uy - 2))
    return framed


def read_json_to_graph(json_file, units='pb'):
    """
    Read a json file with the HIG-20-012 2D (mass and width) format:
    {
        "width1": {
            "mass1": limit1,
            "mass2": limit2,
            ...
        },
        "width2": {
            "mass1": limit1,
            "mass2": limit2,
            ...
        },
        ...
    }
    and return a TGraph2D.
    Seperate jsons are to be provided for observed and expected limits.
    The units of the cross-section should also be specified, either 'pb' or 'fb'.
    """
    masses = []
    widths = []
    limits = []

    if units not in ['pb', 'fb']:
        raise ValueError('Units must be either "pb" or "fb"')
    unit_scale = 1.
    if units == 'fb':
        unit_scale = 1./1000
    else: unit_scale = 1.

    with open(json_file, 'r') as f:
        data = json.load(f)
        for width in data:
            for mass in data[width]:
                masses.append(float(mass))
                if width == '0.1%': widths.append(0.) # 0.1% is used for NWA in HWW so set this to 0 TODO: check if this is the same for other channels
                else: widths.append(float(width.replace('%',''))/100*float(mass))
                limits.append(data[width][mass]*unit_scale)        

    graph = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(limits))
    return graph    


def read_json_to_graphs_NWA(json_file, obs_name='obs', exp_name='exp0', units='pb'):

    """
    Read a json with the standard combine format, where the limits are given as a function of mass only.
    This is intended to be used for analyses where a narrow width approximation is assumed.
    The json should have the following format:
    {
        "mass1": {
            "obs_name": limit1,
            "exp_name": limit2,
            ...
        },
        "mass2": {
            "obs_name": limit1,
            "exp_name": limit2,
            ...
        },
        ...
    }
    where exp_name and obs_name can be set to any value, but by default they are 'exp0' and 'obs' respectively.
    The units of the cross-section should also be specified, either 'pb' or 'fb'.
    Both obsserved and expected limits are read from the same json file. 
    The output is two TGraph2D objects, one for observed and one for expected limits.
    """

    if units not in ['pb', 'fb']:
        raise ValueError('Units must be either "pb" or "fb"')
    unit_scale = 1.
    if units == 'fb':
        unit_scale = 1./1000
    else: unit_scale = 1.

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
            observed.append(data[mass]['obs']*unit_scale)       
            expected.append(data[mass]['exp0']*unit_scale)
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

def read_csv_to_graphs(file_path, mass_column=0, obs_column=2, exp_colum=3, width_column=1, skip_lines=1, units='pb'): # TODO: change defaults to B2G format (currently using format from H->ZZ search)
    
    """
    Read a csv file to get the observed and expected limits as a function of mass and (optionally) width.
    The columns corresponding to the mass, observed, expected and width values should be specified using the mass_column, obs_column, exp_column and width_column arguments.
    If width_column is set to None, it is assumed that the limits are given as a function of mass only (assumes NWA for all widths).
    The units of the cross-section should also be specified, either 'pb' or 'fb'.
    The skip_lines argument is used to skip the header of the csv file (default=1).
    The output is two TGraph2D objects, one for observed and one for expected limits.
    """

    masses = []
    widths = []
    observed = []
    expected = []
    
    if units not in ['pb', 'fb']:
        raise ValueError('Units must be either "pb" or "fb"')
    unit_scale = 1.
    if units == 'fb':
        unit_scale = 1./1000
    else: unit_scale = 1.    
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for i in range(skip_lines): next(reader)  # Skip header
        
        for row in reader:
            mass = float(row[mass_column])
            if width_column is None:
                width = 0. # Assume NWA
            else:
                width = float(row[width_column])
            obs = float(row[obs_column])*unit_scale
            exp = float(row[exp_colum])*unit_scale
            
            masses.append(mass)
            widths.append(width)
            observed.append(obs)
            expected.append(exp)

            #if width_column is None then we also add a 100% width value to the graph with the same limits as the narrow width approximation
            if width_column is None:
                masses.append(mass)
                widths.append(mass)
                observed.append(obs)
                expected.append(exp)
    
    graph_obs = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(observed))
    graph_obs.SetName('g_obs')
    graph_exp = ROOT.TGraph2D(len(masses), np.array(masses), np.array(widths), np.array(expected))
    graph_exp.SetName('g_exp')

    return graph_obs, graph_exp

if __name__ == "__main__":

    root_file = 'mh125EFT_HWW_graphs_gg.root'
    f = ROOT.TFile(root_file)
    h = f.Get('h_excluded_obs')

    contours = contourFromTH2(h,1.)

    fout = ROOT.TFile('HWW_contours.root','RECREATE')
    for i, g in enumerate(contours):
        fout.cd()
        g.Write(f'graph{i}')

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



    filled_region.Write('filled')