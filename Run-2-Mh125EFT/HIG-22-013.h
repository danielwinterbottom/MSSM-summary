#include "TGraph.h"
#include "TFile.h"

TGraph* HIG_22_013_obs(bool filled){
  // get limits directly from ROOT file
  TFile *f = new TFile("mh125EFT_XToTTbar_mAtanb_contours_NN.root");
  TGraph* graph = (TGraph*)f->Get("contour_obs_0");	
  return graph;
}

TGraph* HIG_22_013_exp(){
  // empty for now since no expected scans are provided
  TGraph* graph = new TGraph();
  return graph;
}
