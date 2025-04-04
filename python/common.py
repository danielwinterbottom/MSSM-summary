import ROOT

# Define transparent colors
tRed     = ROOT.TColor(3001,  1.,  0.,  0., "tRed"     , 0.15)
tGreen   = ROOT.TColor(3002,  0.,  1.,  0., "tGreen"   , 0.15)
tBlue    = ROOT.TColor(3003,  0.,  0.,  1., "tBlue"    , 0.15)
tMagenta = ROOT.TColor(3004,  1.,  0.,  1., "tMagenta" , 0.15)
tCyan    = ROOT.TColor(3005,  0.,  1.,  1., "tCyan"    , 0.50)
tYellow  = ROOT.TColor(3006,  1.,  1.,  0., "tYellow"  , 0.15)
tYellowD = ROOT.TColor(3007, 0.5, 0.5,  0., "tYellow"  , 0.15)
tOrange  = ROOT.TColor(3008,  1.,  .5,  0., "tOrange"  , 0.15)
tBlack   = ROOT.TColor(3009,  0.,  0.,  0., "tBlack"   , 0.15)
kCombDark= ROOT.TColor(3010, .48, .88,  1., "kCombDark")
kComb    = ROOT.TColor(3011, .28, .58, .70, "kComb")
tComb    = ROOT.TColor(3012, .28, .58, .70, "tComb"    , 0.25)

# Common plotting style for expected and observed limit contours
#  exp         : TGraph for expected limits
#  obs         : TGraph for observed limits
#  dcolor      : fill (=hatch) color for expected limits
#  lcolor      : line color for observed limits
#  tcolor      : (transparent) fill color for observed limits
#  upper_limit : indicate whether these are upper/lower limits (for hatching)

# Canvas for a squared central figure with legend to the right including "CMS and lumi" tag
def squared_legend_to_right(lower_x=130., upper_x=1000, lower_y=-0.5, upper_y=0.5, log_x=0, log_y=0, preliminary=True, x_title='m_{H} [GeV]', y_title='sin#alpha'):
  canv = ROOT.TCanvas("canv", "Limits", 900, 640)
  canv.SetGridx(0)
  canv.SetGridy(0)
  canv.SetLogx(log_x)
  canv.SetLogy(log_y)
  canv.SetLeftMargin(0.12)
  canv.SetRightMargin(0.35)
  canv.SetTopMargin(0.06)
  canv.SetBottomMargin(0.10)
  hr = canv.DrawFrame(lower_x, lower_y, upper_x, upper_y)
  # define x-axis
  hr.SetXTitle(x_title)
  hr.GetXaxis().SetLabelFont(42)
  hr.GetXaxis().SetLabelSize(0.034)
  hr.GetXaxis().SetLabelOffset(0.015)
  hr.GetXaxis().SetTitleSize(0.04)
  hr.GetXaxis().SetTitleFont(42)
  hr.GetXaxis().SetTitleColor(1)
  hr.GetXaxis().SetTitleOffset(1.20)
  hr.GetXaxis().SetNdivisions(50005)
  hr.GetXaxis().SetMoreLogLabels()
  hr.GetXaxis().SetNoExponent()
  # define y-axis
  hr.SetYTitle(y_title)
  hr.GetYaxis().SetLabelFont(42)
  hr.GetYaxis().SetTitleSize(0.04)
  hr.GetYaxis().SetTitleOffset(0.9)
  hr.GetYaxis().SetLabelSize(0.034)
  hr.GetYaxis().SetNdivisions(50005)
  hr.GetYaxis().SetMoreLogLabels()

  tex = ROOT.TLatex()
  tex.SetNDC()
  tex.SetTextAlign(11)

  tex.SetTextFont(63)
  tex.SetTextSize(25)
  tex.SetTextAngle( 0)
  tex.SetTextColor(ROOT.kBlack)
  tex.DrawLatex(0.12, 0.95, "CMS")
  if preliminary:
    tex.SetTextFont(53)
    tex.SetTextSize(25)
    tex.DrawLatex(0.19, 0.95, "Preliminary")
  tex.SetTextFont(42)
  tex.SetLineWidth(2)
  tex.SetTextSize(0.035)
  tex.DrawLatex(0.49,0.95,"138 fb^{-1} (13 TeV)")

  return canv
