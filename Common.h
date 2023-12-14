#include <iostream>

#include "TROOT.h"
#include "TColor.h"
#include "TCanvas.h"
#include "TPaveText.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TH2F.h"

// Define transparent colors
TColor* tRed     = new TColor(3001,  1.,  0.,  0., "tRed"     , 0.15);
TColor* tGreen   = new TColor(3002,  0.,  1.,  0., "tGreen"   , 0.15);
TColor* tBlue    = new TColor(3003,  0.,  0.,  1., "tBlue"    , 0.15);
TColor* tMagenta = new TColor(3004,  1.,  0.,  1., "tMagenta" , 0.15);
TColor* tCyan    = new TColor(3005,  0.,  1.,  1., "tCyan"    , 0.50);
TColor* tYellow  = new TColor(3006,  1.,  1.,  0., "tYellow"  , 0.15);
TColor* tYellowD = new TColor(3007, 0.5, 0.5,  0., "tYellow"  , 0.15);
TColor* tOrange  = new TColor(3008,  1.,  .5,  0., "tOrange"  , 0.15);
TColor* tBlack   = new TColor(3009,  0.,  0.,  0., "tBlack"   , 0.15);
TColor* kCombDark= new TColor(3010, .48, .88,  1., "kCombDark");
TColor* kComb    = new TColor(3011, .28, .58, .70, "kComb");
TColor* tComb    = new TColor(3012, .28, .58, .70, "tComb"    , 0.25);
 
// Common plotting style for expected and observed limit contours 
//  exp         : TGraph for expected limits
//  obs         : TGraph for observed limits
//  dcolor      : fill (=hatch) color for expected limits
//  lcolor      : line color for observed limits
//  tcolor      : (transparent) fill color for observed limits
//  upper_limit : indicate whether these are upper/lower limits (for hatching)  
// TGraph* of the observed limit contour is returned.
TGraph* Contour(TGraph* exp(), TGraph* obs(bool), int dcolor, int lcolor, int tcolor, bool upper_limit=true){
  TGraph* g0=0; 
  TGraph* g1=0;
  if(exp){
    g0 = exp();
    g0->SetLineColor(dcolor);
    g0->SetLineWidth((upper_limit?+1:-1)*303);
    g0->SetFillStyle(3004);
    g0->SetFillColor(dcolor);
    g0->SetLineStyle(1);
    g0->Draw("Lsame");
  }
  if(obs){
    g1 = obs(true );
    TGraph* g2 = obs(false);
    g2->SetLineColor(lcolor);
    g2->SetLineStyle(1);
    g2->SetLineWidth(1);
    g2->SetMarkerStyle(20);
    g2->SetMarkerSize(0.7);
    g2->SetMarkerColor(lcolor);
    g1->SetLineColor(lcolor);
    g1->SetFillColor(tcolor);
    g1->SetFillStyle(1001);
    g1->Draw("Fsame");
    g2->Draw("Lsame");
  }
  return g1 ? g1 : g0;
}

// Canvas for a squared central figure with legend to the right including "CMS and lumi" tag
TCanvas* squared_legend_to_right(float lower_x=130., float upper_x=2100., float lower_y=1., float upper_y=60., int log_x=1, int log_y=1){
  TCanvas* canv = new TCanvas("MSSM", "MSSM Limits", 900, 640);
  canv->SetGridx(0); canv->SetLogx(log_x);
  canv->SetGridy(0); canv->SetLogy(log_y);
  canv->SetLeftMargin(0.12);
  canv->SetRightMargin(0.35);
  canv->SetTopMargin(0.06);
  canv->SetBottomMargin(0.10);  
  TH1F* hr=canv->DrawFrame(lower_x, lower_y, upper_x, upper_y);
  // define x-axis
  hr->SetXTitle("m_{A} [GeV]");
  hr->GetXaxis()->SetLabelFont(42);
  hr->GetXaxis()->SetLabelSize(0.034);
  hr->GetXaxis()->SetLabelOffset(0.015);
  hr->GetXaxis()->SetTitleSize(0.04);
  hr->GetXaxis()->SetTitleFont(42);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.20);
  hr->GetXaxis()->SetNdivisions(50005);
  hr->GetXaxis()->SetMoreLogLabels();
  hr->GetXaxis()->SetNoExponent();
  // define y-axis
  hr->SetYTitle("tan#beta");
  hr->GetYaxis()->SetLabelFont(42);
  hr->GetYaxis()->SetTitleSize(0.04);
  hr->GetYaxis()->SetTitleOffset(0.9);
  hr->GetYaxis()->SetLabelSize(0.034);    
  hr->GetYaxis()->SetNdivisions(50005);
  hr->GetYaxis()->SetMoreLogLabels();

  TLatex* tex;
  tex = new TLatex();
  tex->SetNDC();
  tex->SetTextAlign(11);

  tex->SetTextFont(63);
  tex->SetTextSize(25);
  tex->SetTextAngle( 0);
  tex->SetTextColor(kBlack);
  tex->DrawLatex(0.12, 0.95, "CMS");
  tex->SetTextFont(53);
  tex->SetTextSize(25);
  tex->DrawLatex(0.19, 0.95, "Preliminary");
  tex->SetTextFont(42);
  tex->SetLineWidth(2);
  tex->SetTextSize(0.035);
  tex->DrawLatex(0.42,0.95,"35.9-138 fb^{-1} (13 TeV)");

  return canv;
}

