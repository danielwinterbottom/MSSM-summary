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
parser.add_argument('--tanb', type=float, default=1.0, help='The value of tan(beta)')

args = parser.parse_args()

xsbr_tool = SingletXSBRs()

print (f"Processing widths for tanb={args.tanb}")

mH_range = (100,1500)
sina_range = (-0.5,0.5)

h_widths = ROOT.TH2D('h_widths','',1000,mH_range[0],mH_range[1],1000,sina_range[0],sina_range[1])

for y in range(1,h_widths.GetNbinsY()+1):
    for x in range(1,h_widths.GetNbinsX()+1):

        sina = h_widths.GetYaxis().GetBinCenter(y)
        mH   = h_widths.GetXaxis().GetBinCenter(x)

        width = xsbr_tool.ComputeWidth(mH, args.tanb, sina)

        rel_width = width / mH if mH != 0 else 0.

        h_widths.SetBinContent(x,y,rel_width)

benchmark_name = f'singlet_tanb{args.tanb}'.replace('.','p')

fout = ROOT.TFile(f'{benchmark_name}_widths_vs_mHsina.root', 'recreate')

#contoursList = [0.05, 0.1, 0.15, 0.20]
#contours = array('d', contoursList)
#h_widths.SetContour(len(contours), contours)

h_widths.Write('widths_tanb'+str(args.tanb).replace('.','p'))

contours_0p01 = contourFromTH2(h_widths, threshold=0.01)
contours_0p05 = contourFromTH2(h_widths, threshold=0.05)
contours_0p1 = contourFromTH2(h_widths, threshold=0.1)
contours_0p15 = contourFromTH2(h_widths, threshold=0.15)
contours_0p20 = contourFromTH2(h_widths, threshold=0.20)

contours_0p01 = sorted(contours_0p01, key=lambda x: x.GetN(), reverse=True)
contours_0p05 = sorted(contours_0p05, key=lambda x: x.GetN(), reverse=True)
contours_0p1 = sorted(contours_0p1, key=lambda x: x.GetN(), reverse=True)
contours_0p15 = sorted(contours_0p15, key=lambda x: x.GetN(), reverse=True)
contours_0p20 = sorted(contours_0p20, key=lambda x: x.GetN(), reverse=True)

# now write all contours to the output file
for i, c in enumerate(contours_0p01):
    c.Write(f"contours_0p01_tanb{str(args.tanb).replace('.','p')}_{i}")
for i, c in enumerate(contours_0p05):
    c.Write(f"contours_0p05_tanb{str(args.tanb).replace('.','p')}_{i}")
for i, c in enumerate(contours_0p1):
    c.Write(f"contours_0p1_tanb{str(args.tanb).replace('.','p')}_{i}")
for i, c in enumerate(contours_0p15):
    c.Write(f"contours_0p15_tanb{str(args.tanb).replace('.','p')}_{i}")
for i, c in enumerate(contours_0p20):
    c.Write(f"contours_0p20_tanb{str(args.tanb).replace('.','p')}_{i}")

fout.Close()