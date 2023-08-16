/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_18_005_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 223.29, 2.01);
  graph->SetPoint( 1, 233.54, 2.96);
  graph->SetPoint( 2, 238.30, 2.99);
  graph->SetPoint( 3, 243.43, 2.77);
  graph->SetPoint( 4, 248.18, 2.73);
  graph->SetPoint( 5, 253.67, 2.92);
  graph->SetPoint( 6, 263.19, 2.92);
  graph->SetPoint( 7, 273.44, 2.97);
  graph->SetPoint( 8, 281.13, 2.93);
  graph->SetPoint( 9, 295.77, 3.37);
  graph->SetPoint(10, 308.58, 3.81);
  graph->SetPoint(11, 317.17, 3.85);
  graph->SetPoint(12, 328.71, 3.52);
  graph->SetPoint(13, 338.59, 3.69);
  graph->SetPoint(14, 348.47, 2.65);
  graph->SetPoint(15, 358.72, 2.26);
  if(filled){
    graph->SetPoint(16, 358.72, 1.00);
    graph->SetPoint(17, 223.29, 1.00);
    graph->SetPoint(18, 223.29, 2.01);
  }
  return graph;
}

TGraph* HIG_18_005_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 223.29, 2.15);
  graph->SetPoint( 1, 233.54, 2.64);
  graph->SetPoint( 2, 238.30, 2.75);
  graph->SetPoint( 3, 243.43, 2.85);
  graph->SetPoint( 4, 248.18, 2.89);
  graph->SetPoint( 5, 253.67, 2.95);
  graph->SetPoint( 6, 263.19, 3.09);
  graph->SetPoint( 7, 273.44, 3.16);
  graph->SetPoint( 8, 281.13, 3.22);
  graph->SetPoint( 9, 295.77, 3.37);
  graph->SetPoint(10, 308.58, 3.48);
  graph->SetPoint(11, 317.17, 3.58);
  graph->SetPoint(12, 328.71, 3.75);
  graph->SetPoint(13, 338.59, 3.96);
  graph->SetPoint(14, 348.47, 2.50);
  graph->SetPoint(15, 358.72, 1.56);
  return graph;
}
