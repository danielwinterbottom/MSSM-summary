#include "TGraph.h"
#include "TFile.h"

TGraph* B2G_23_002_obs(bool filled){
 // get limits directly from ROOT file
 TFile *f = new TFile("mh125_ggToHTohh_mAtanb_contours.root");
 TGraph* graph = (TGraph*)f->Get("contour_obs_0"); 

  return graph;
}

TGraph* B2G_23_002_exp(){

  TFile *f = new TFile("mh125_ggToHTohh_mAtanb_contours.root");
  TGraph* graph = (TGraph*)f->Get("contour_exp_0");

  return graph;
}




























