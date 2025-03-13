#include "TGraph.h"
#include "TFile.h"

TGraph* HIG_20_016_obs(bool filled){
 // get limits directly from ROOT file
 TFile *f = new TFile("mh125_ggToHToWW_mAtanb_contours.root");
 TGraph* graph = (TGraph*)f->Get("contour_obs_1"); // note contour 1 is used here as 0 is an unphysical region at low mA

  return graph;
}

TGraph* HIG_20_016_exp(){

  TFile *f = new TFile("mh125_ggToHToWW_mAtanb_contours.root");
  TGraph* graph = (TGraph*)f->Get("contour_exp_0");

  return graph;
}




























