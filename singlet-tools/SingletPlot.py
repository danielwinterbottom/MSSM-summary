import ROOT
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../python")
from common import *
import argparse
ROOT.gROOT.SetBatch(True)
import numpy as np

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

f_ww = ROOT.TFile(f'singlet_tanb{tanb_str}_ggToHToWW_mHsina_contours.root')
h_ww_obs = f_ww.Get('h_obs_excluded')
h_ww_exp = f_ww.Get('h_exp_excluded')

canv = squared_legend_to_right()

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
sina_lim_obs = np.sin(np.acos(low_lim**.5)) # XS scales like sina^2. All partial widths scale by sina^2 so BRs will stay the same

low_lim = 1.00-0.053*2 # 95% lower limit
sina_lim_exp = np.sin(np.acos(low_lim**.5)) # XS scales like sina^2. All partial widths scale by sina^2 so BRs will stay the same

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

g1=DrawObsHist(h_ww_obs, tYellow.GetNumber(),ROOT.kYellow+2)
DrawExpHist(h_ww_exp, ROOT.kYellow+2)

g2=DrawObsHist(h_zz_obs, tMagenta.GetNumber(),ROOT.kMagenta)
DrawExpHist(h_zz_exp, ROOT.kMagenta+2)

g3=DrawObsHist(h_hh_obs, tRed.GetNumber(),ROOT.kRed)
DrawExpHist(h_hh_exp, ROOT.kRed+2)

leg = ROOT.TLegend(0.67, 0.10, 0.97, 0.94)
leg.SetHeader("tan#beta = %.1f" % args.tanb,"C")
leg.SetBorderSize(1)
leg.SetFillStyle(1001)
leg.SetTextSize(0.036)
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
leg.AddEntry(g3,"#splitline{H#rightarrow hh}{arXiv:2403.16926}","F")
leg.AddEntry(g_sm_h_obs_up,"#splitline{h(125)}{HIG-21-018}","F")
leg.Draw()


canv.Update()
canv.Print(f"Singlet_limits_tanb{tanb_str}.pdf")
