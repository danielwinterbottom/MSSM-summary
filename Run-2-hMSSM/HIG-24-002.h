#include "TGraph.h"
#include "TFile.h"

TGraph* HIG_24_002_obs(bool filled){
 // get limits directly from ROOT file
 TFile *f = new TFile("hMSSM_ggToHToZZ_mAtanb_contours.root");
 TGraph* graph = (TGraph*)f->Get("contour_obs_0"); 

  return graph;
}

TGraph* HIG_24_002_exp(){

  TFile *f = new TFile("hMSSM_ggToHToZZ_mAtanb_contours.root");
  TGraph* graph = (TGraph*)f->Get("contour_exp_0");

  return graph;
}




























