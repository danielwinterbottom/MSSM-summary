#include "../Common.h"
#include "HIG-16-018.h"
#include "HIG-17-002.h"
#include "HIG-21-001.h"
#include "HIG-21-005.h"
#include "HIG-21-011.h"
#include "HIG-20-016.h"
#include "HIG-17-027.h"
#include "HIG-17-031.h"
#include "HIG-17-033.h"
#include "HIG-18-010.h"
#include "HIG-18-023.h"

void MSSM_limits_hMSSM(){
/*-----------------------------------------------------------------------------

 General setup of the canvas

-----------------------------------------------------------------------------*/
  // switch off stats box
  gStyle->SetOptStat(0);
  // define canvas  
  TCanvas* canv = squared_legend_to_right(130., 2000.);
  // define legend
  TLegend* leg0_ = new TLegend(0.67, 0.10, 0.97, 0.94);
  leg0_->SetBorderSize(1);
  leg0_->SetFillStyle (1001);
  leg0_->SetTextSize(0.026);
  leg0_->SetFillColor (kWhite);
  TGraph* obs = new TGraph(); obs->SetFillColor(kGray);
  TGraph* exp = new TGraph(); 
  exp->SetLineColor(1.); 
  exp->SetFillColor(1.); 
  exp->SetLineWidth(303); 
  exp->SetFillStyle(3004);     
  leg0_->AddEntry(obs, "Observed exclusion 95% CL", "F");  
  leg0_->AddEntry(exp, "Expected exclusion 95% CL", "LF");
  
/*-----------------------------------------------------------------------------

 Plotting (contours will be drawn on top of each other according to this order)

-----------------------------------------------------------------------------*/
  TGraph* g1 = Contour(HIG_17_031_exp, HIG_17_031_obs, kCombDark->GetNumber(), kComb->GetNumber(), tComb->GetNumber(),false); 
  leg0_->AddEntry(g1 , "#splitline{h(125)}{EPJC 79 (2019) 421}", "F");
  TGraph* g2 = Contour(HIG_21_001_exp, HIG_21_001_obs, kBlue+2, kBlue, tBlue->GetNumber(), true); 
  leg0_->AddEntry(g2, "#splitline{A/H/h #rightarrow #tau#tau}{arxiv:2208.02717^{#scale[1.6]{ #club}}}", "F");
  TGraph* g3 = Contour(HIG_20_016_exp, HIG_20_016_obs, kMagenta+2, kMagenta, tMagenta->GetNumber(), false); 
  leg0_->AddEntry(g3, "#splitline{H #rightarrow WW(2l2#nu)}{(HIG-20-016)^{#scale[1.6]{ #club}}}", "F");
  TGraph* g4 = Contour(HIG_21_011_exp, HIG_21_011_obs, kRed+2, kRed, tRed->GetNumber(), false); 
  leg0_->AddEntry(g4 , "#splitline{H #rightarrow hh (bb#gamma#gamma)}{(HIG-21-011)^{#scale[1.6]{ #club}}}", "F");
  TGraph* g5 = Contour(HIG_21_005_exp, HIG_21_005_obs, kGreen+2, kGreen, tGreen->GetNumber(), false); 
  leg0_->AddEntry(g5 , "#splitline{H #rightarrow hh (bbWW)}{(HIG-21-005)^{#scale[1.6]{ #club}}}", "F");
  TGraph* g6 = Contour(HIG_18_023_exp, HIG_18_023_obs, kYellow+2, kYellow, tYellow->GetNumber(), false); 
  leg0_->AddEntry(g6, "#splitline{A #rightarrow Zh (ll#tau#tau)}{JHEP 03 (2020) 65}", "F");
  TGraph* g7 = Contour(HIG_17_027_exp, HIG_17_027_obs, kOrange+2, kOrange, tOrange->GetNumber(), false); 
  leg0_->AddEntry(g7, "#splitline{H/A #rightarrow tt}{JHEP 04 (2020) 171}", "F");

/*-----------------------------------------------------------------------------

 Labelling

-----------------------------------------------------------------------------*/  
  
  TPaveText* extra = new TPaveText(0.55, 0.85, 0.65, 0.95, "NDC");
  extra->SetBorderSize(   0 );
  extra->SetFillStyle (   0 );
  extra->SetTextAlign (  12 );
  extra->SetTextSize  (0.03 );
  extra->SetTextColor (   1 );
  extra->SetTextFont  (  62 );
  extra->AddText("hMSSM");
  extra->Draw("same");  

  leg0_->Draw("same");
  TLatex* tex;
  tex = new TLatex();
  tex->SetNDC();
  tex->SetTextAlign(11);
  tex->SetTextFont(43);
  tex->SetTextSize(20);
  tex->DrawLatex(0.88, 0.057, "^{#scale[1.4]{#club}} 138 fb^{-1}");
  tex->DrawLatex(0.105, 0.057, "130");

  canv->Update();
  canv->Print("MSSM_limits_hMSSM.pdf");
  return;
}

