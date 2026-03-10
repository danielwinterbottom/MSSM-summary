import ROOT
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../python")
from common import *
import argparse
ROOT.gROOT.SetBatch(True)
import numpy as np
import math
from ctypes import c_double

parser = argparse.ArgumentParser()
parser.add_argument('--tanb', type=float, default=1.0, help='The value of tan(beta)')
args = parser.parse_args()

tanb_str = ('%.1f' % args.tanb).replace('.','p')

f_zz = ROOT.TFile(f'singlet_tanb{tanb_str}_ggToHToZZ_mHsina_contours.root')
h_zz_obs = f_zz.Get('h_obs_excluded')
h_zz_exp = f_zz.Get('h_exp_excluded')

f_hh = ROOT.TFile(f'singlet_tanb{tanb_str}_ggToHTohh_mHsina_contours.root')
h_hh_obs = f_hh.Get('h_obs_excluded')
h_hh_exp = f_hh.Get('h_exp_excluded')

# f_ww = ROOT.TFile(f'singlet_tanb{tanb_str}_gg+vbfToHToWW_mHsina_contours.root')
f_ww = ROOT.TFile(f'singlet_tanb{tanb_str}_ggToHToWW_mHsina_contours.root')
h_ww_obs = f_ww.Get('h_obs_excluded')
h_ww_exp = f_ww.Get('h_exp_excluded')

sina_limit = 0.4

canv = squared_legend_to_right(lower_y=-sina_limit, upper_y=sina_limit)

def DrawObsHist(hist, tcolor, lcolor):
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("")
    hist.GetYaxis().SetTitle("")
    hist.SetFillColor(tcolor)
    hist.Draw("BOXsame")
    hist.SetLineColor(lcolor)
    hist.SetContour(1,np.array([0.5]))
    hist.Draw("CONT3same")
    g = ROOT.TGraph()
    g.SetLineColor(lcolor)
    g.SetFillColor(tcolor)

    return g

def DrawExpHist(hist,lcolor):
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("")
    hist.GetYaxis().SetTitle("")
    hist.SetLineColor(lcolor)
    hist.SetContour(1,np.array([0.5]))
    hist.SetLineWidth(2)
    hist.Draw("CONT3same")


# take SM H125 measurments of inclusive mu from HIG-21-018 and use these to set a limit on sina
# obs = 1.014 +0.055 -0.053
low_lim = 1.014-0.053*2 # 95% lower limit
sina_lim_obs = np.sin(math.acos(low_lim**.5)) # XS scales like sina^2. All partial widths scale by sina^2 so BRs will stay the same

low_lim = 1.00-0.053*2 # 95% lower limit
sina_lim_exp = np.sin(math.acos(low_lim**.5)) # XS scales like sina^2. All partial widths scale by sina^2 so BRs will stay the same

g_sm_h_obs_up = ROOT.TGraph()
g_sm_h_obs_up.SetPoint(0,0.,1.0)
g_sm_h_obs_up.SetPoint(1,0.,sina_lim_obs)
g_sm_h_obs_up.SetPoint(2,100000.,sina_lim_obs)
g_sm_h_obs_up.SetPoint(3,100000.,1.0)
g_sm_h_obs_up.SetPoint(4,0.,1.0)

g_sm_h_obs_down = ROOT.TGraph()
g_sm_h_obs_down.SetPoint(0,0.,-1.0)
g_sm_h_obs_down.SetPoint(1,0.,-sina_lim_obs)
g_sm_h_obs_down.SetPoint(2,100000.,-sina_lim_obs)
g_sm_h_obs_down.SetPoint(3,100000.,-1.0)
g_sm_h_obs_down.SetPoint(4,0.,-1.0)

g_sm_h_exp_up = ROOT.TGraph()
g_sm_h_exp_up.SetPoint(0,0.,sina_lim_exp)
g_sm_h_exp_up.SetPoint(1,100000.,sina_lim_exp)

g_sm_h_exp_down = ROOT.TGraph()
g_sm_h_exp_down.SetPoint(0,0.,-sina_lim_exp)
g_sm_h_exp_down.SetPoint(1,100000.,-sina_lim_exp)

def PlotGraphObs(g, lcolor, tcolor):
    g.SetLineColor(lcolor)
    g.SetLineStyle(1)
    g.SetLineWidth(1)
    g.SetMarkerColor(lcolor)
    g.SetLineColor(lcolor)
    g.SetFillColor(tcolor)
    g.SetFillStyle(1001)
    g.Draw("Fsame")
    g.Draw("Lsame")

def PlotGraphExp(g, lcolor):
    g.SetLineColor(lcolor)
    g.SetLineWidth(2)
    g.SetFillStyle(0)
    g.SetLineStyle(1)
    g.Draw("Csame")

PlotGraphObs(g_sm_h_obs_up, kComb.GetNumber(), tComb.GetNumber())
PlotGraphObs(g_sm_h_obs_down, kComb.GetNumber(), tComb.GetNumber())
PlotGraphExp(g_sm_h_exp_up, kCombDark.GetNumber())
PlotGraphExp(g_sm_h_exp_down, kCombDark.GetNumber())

g1=DrawObsHist(h_ww_obs, tGreen.GetNumber(),ROOT.kGreen)
DrawExpHist(h_ww_exp, ROOT.kGreen+2)

g2=DrawObsHist(h_zz_obs, tMagenta.GetNumber(),ROOT.kMagenta)
DrawExpHist(h_zz_exp, ROOT.kMagenta+2)

g3=DrawObsHist(h_hh_obs, tRed.GetNumber(),ROOT.kRed)
DrawExpHist(h_hh_exp, ROOT.kRed+2)

# draw iso-width lines
f_width = ROOT.TFile(os.path.dirname(os.path.abspath(__file__))+'/singlet_widths.root')
tanb_str = str(args.tanb).replace('.','p')
# check if any TGraphs exist named contours_tanb{tanb_str}_0p05_{i} and contours_tanb{tanb_str}_0p1_{i} for i >=0
contours_0p05 = []
for i in range(4): # up to 4 contours but usually only 1 will exist
    c_0p05 = f_width.Get(f'contours_0p05_tanb{tanb_str}_{i}')
    if c_0p05: contours_0p05.append(c_0p05)

def DrawContourLabel(c, label_text):

    # Choose a point (e.g., the midpoint) to place the label
    # find a value of a point within the displayed axis limits
    # loop over all points in the graph, and find those withing the axis-limits
    # then take the middle point

    x_min, x_max = 125,1000
    y_min, y_max = 0, sina_limit
    points_in_range = []
    for i in range(c.GetN()):
        x, y = c_double(), c_double()
        c.GetPoint(i, x, y)
        x = float(x.value)
        y = float(y.value)
        if x_min <= x <= x_max and y_min <= y <= y_max:
            points_in_range.append((x, y))
    # sort points by x value
    points_in_range.sort(key=lambda p: p[0])  # sort by x value
            
    # pick a point near to xmax
    if points_in_range:
        index = len(points_in_range)-1  # take a point near the end
        #mid_index = len(points_in_range) // 1.5
        x, y = points_in_range[index]

        # Create and draw a label at that point
        label = ROOT.TLatex(x-10, y-0.045, label_text)
        # get angle based on the slope of the line
        if index > 0:
            x_prev, y_prev = points_in_range[index-10]
            angle = math.degrees(math.atan2(y - y_prev, x - x_prev)) * 1500
            label.SetTextAngle(angle)
        label.SetTextSize(0.03)
        # align the label to the right
        label.SetTextAlign(30)  # 1 = left, 2 = center
        label.SetTextColor(ROOT.kBlack)
        return label

for c in contours_0p05:
    c.SetLineColor(ROOT.kBlack)
    c.SetLineWidth(2)
    c.SetLineStyle(5)
    c.Draw("Lsame")

    # Choose a point (e.g., the midpoint) to place the label
    # find a value of a point within the displayed axis limits
    # loop over all points in the graph, and find those withing the axis-limits
    # then take the middle point

    tex = DrawContourLabel(c, '#Gamma_{H}/m_{H}<5%')
    if tex: tex.Draw()


leg = ROOT.TLegend(0.67, 0.10, 0.97, 0.94)
leg.SetHeader("tan#beta = %.1f" % args.tanb,"C")
leg.SetBorderSize(1)
leg.SetFillStyle(1001)
leg.SetTextSize(0.035)
leg.SetFillColor(ROOT.kWhite)
obs = ROOT.TGraph()
obs.SetFillColor(ROOT.kGray)
exp = ROOT.TGraph()
exp.SetLineColor(1)
exp.SetFillColor(1)
exp.SetLineWidth(303)
exp.SetFillStyle(3004)
leg.AddEntry(obs, "#splitline{Observed}{exclusion 95% CL}", "F")
leg.AddEntry(exp, "#splitline{Expected}{exclusion 95% CL}", "L")

leg.AddEntry(g1,"#splitline{H #rightarrow WW}{HIG-20-016}","F")
leg.AddEntry(g2,"#splitline{H #rightarrow ZZ}{HIG-24-002}","F")
leg.AddEntry(g3,"#splitline{H#rightarrow hh [resonant only]}{#splitline{Phys. Rep. 1115}{(2025) 368}}","F")
leg.AddEntry(g_sm_h_obs_up,"#splitline{h(125)}{HIG-21-018}","F")
leg.Draw()


canv.Update()
canv.Print(f"Singlet_limits_tanb{tanb_str}.pdf")
