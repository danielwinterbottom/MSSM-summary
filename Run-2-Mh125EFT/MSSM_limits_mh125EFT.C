#include "../Common.h"
#include "B2G-23-002.h"
#include "HIG-18-005.h"
#include "HIG-18-023.h"
#include "HIG-17-033.h"
#include "HIG-21-001.h"
#include "Eligibility.h"


void MSSM_limits_mh125EFT(){
/*-----------------------------------------------------------------------------

 General setup of the canvas

-----------------------------------------------------------------------------*/
  // switch off stats box
  gStyle->SetOptStat(0);
  // define canvas  
  TCanvas* canv = squared_legend_to_right(90., 1400., 1., 10.);
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
  // eligibility line for the given benchmark
  TGraph* e1 = Eligibility();
  e1->SetLineColor(kGray+1);
  e1->SetLineWidth(1);
  e1->SetLineStyle(1);
  e1->SetLineWidth(2);
  e1->SetFillColor(kGray+1);  
  e1->SetFillStyle(3002);//3005
  e1->Draw("FLsame");

  /*-------------------------------------------------------------------------*/ 
  TGraph* g1 = Contour(HIG_21_001_exp, HIG_21_001_obs, kBlue+2, kBlue, tBlue->GetNumber(), true); 
  leg0_->AddEntry(g1, "#splitline{#phi #rightarrow #tau#tau}{JHEP 07 (2023) 73^{#scale[1.6]{ #club}}}", "F");
  TGraph* g2 = Contour(HIG_17_033_exp, HIG_17_033_obs, kMagenta+2, kMagenta, tMagenta->GetNumber(), false); 
  leg0_->AddEntry(g2, "#splitline{H #rightarrow WW}{JHEP 03 (2020) 34}", "F");
  TGraph* g3 = Contour(HIG_18_005_exp, HIG_18_005_obs, kGreen+2, kGreen, tGreen->GetNumber(), false); 
  leg0_->AddEntry(g3, "#splitline{A #rightarrow ZH(bb)}{EPJ C79 (2019) 564}", "F");
  TGraph* g4 = Contour(HIG_18_023_exp, HIG_18_023_obs, kRed+2, kRed, tRed->GetNumber(), false); 
  leg0_->AddEntry(g4, "#splitline{A #rightarrow ZH(#tau#tau)}{JHEP 03 (2020) 65}", "F");
  /*-------------------------------------------------------------------------*/ 
  /* Preview B2G-23-002                                                      */
  TGraph* g5 = Contour(B2G_23_002_exp, NULL, kYellow+2, kYellow, tYellow->GetNumber(), false); 
  leg0_->AddEntry(g5 , "#splitline{X#rightarrow HH}{B2G-23-002^{#scale[1.6]{ #club}}}", "F");
    
  TGraph* dummy = new TGraph();  
  dummy->SetFillColor(kWhite);
  dummy->SetLineColor(kWhite);
  leg0_->AddEntry(dummy, "", "F");  
  //leg0_->AddEntry(dummy, "", "F");  
  
/*-----------------------------------------------------------------------------

 Labeling

-----------------------------------------------------------------------------*/

  TLegend* leg1_ = new TLegend(0.14, 0.13, 0.34, 0.18);
  leg1_->SetBorderSize(1);
  leg1_->SetFillStyle (1001);
  leg1_->SetTextSize(0.022464);
  leg1_->SetFillColor (kWhite);
  leg1_->AddEntry(e1, "m_{h}^{MSSM}\\neq 125 \\pm 3 GeV", "LF");  

  TPaveText* extra = new TPaveText(0.585, 0.85, 0.685, 0.95, "NDC");
  extra->SetBorderSize(   0 );
  extra->SetFillStyle (   0 );
  extra->SetTextAlign (  12 );
  extra->SetTextSize  (0.03 );
  extra->SetTextColor (   1 );
  extra->SetTextFont  (  62 );
  extra->AddText("M_{h, EFT}^{125}");
  extra->Draw("same");  

  leg0_->Draw("same");
  TLatex* tex;
  tex = new TLatex();
  tex->SetNDC();
  tex->SetTextAlign(11);
  tex->SetTextFont(43);
  tex->SetTextSize(20);
  tex->DrawLatex(0.88, 0.057, "^{#scale[1.4]{#club}} 138 fb^{-1}");
  leg1_->Draw("same");

  canv->Update();
  canv->Print("MSSM_limits_mh125EFT.pdf");
  return;
}

