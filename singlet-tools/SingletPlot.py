import ROOT
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../python")
from common import *
import argparse
ROOT.gROOT.SetBatch(True)
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--tanb', type=str, default='1p0', help='The value of tan(beta)')
args = parser.parse_args()

f_zz = ROOT.TFile(f'singlet_tanb{args.tanb}_ggToHToZZ_mHsina_contours.root')
h_zz_obs = f_zz.Get('h_obs_excluded')
h_zz_exp = f_zz.Get('h_exp_excluded')

f_hh = ROOT.TFile(f'singlet_tanb{args.tanb}_ggToHTohh_mHsina_contours.root')
h_hh_obs = f_hh.Get('h_obs_excluded')
h_hh_exp = f_hh.Get('h_exp_excluded')

f_ww = ROOT.TFile(f'singlet_tanb{args.tanb}_ggToHToWW_mHsina_contours.root')
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

def DrawExpHist(hist,lcolor):
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("")
    hist.GetYaxis().SetTitle("")
    hist.SetLineColor(lcolor)
    hist.SetContour(1,np.array([0.5]))
    hist.SetLineWidth(2)
    hist.Draw("CONT3same")

DrawObsHist(h_ww_obs, tCyan.GetNumber(),ROOT.kCyan)
DrawExpHist(h_ww_exp, ROOT.kCyan+2)

DrawObsHist(h_zz_obs, tMagenta.GetNumber(),ROOT.kMagenta)
DrawExpHist(h_zz_exp, ROOT.kMagenta+2)

DrawObsHist(h_hh_obs, tRed.GetNumber(),ROOT.kRed)
DrawExpHist(h_hh_exp, ROOT.kRed+2)

canv.Update()
canv.Print(f"Singlet_limits_tanb{args.tanb}.pdf")
