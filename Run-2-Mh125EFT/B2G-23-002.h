#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 200.71, 2.59);
  graph->SetPoint( 1, 234.38, 5.72);
  graph->SetPoint( 2, 253.52, 5.83);
  graph->SetPoint( 3, 337.66, 5.22);
  graph->SetPoint( 4, 384.85, 5.15);
  graph->SetPoint( 5, 452.09, 4.33);
  graph->SetPoint( 6, 509.11, 3.34);
  graph->SetPoint( 7, 562.56, 2.80);
  graph->SetPoint( 8, 587.96, 2.43);
  graph->SetPoint( 9, 613.80, 2.11);
  graph->SetPoint(10, 641.87, 1.85);
  graph->SetPoint(11, 652.56, 1.80);
  graph->SetPoint(12, 683.76, 1.46);
  graph->SetPoint(13, 744.36, 1.00);
  if(filled){
    graph->SetPoint(14, 200.71, 1.00);
    graph->SetPoint(15, 200.71, 2.59);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 200.71, 2.59);
  graph->SetPoint( 1, 234.38, 5.72);
  graph->SetPoint( 2, 253.52, 5.83);
  graph->SetPoint( 3, 337.66, 5.22);
  graph->SetPoint( 4, 384.85, 5.15);
  graph->SetPoint( 5, 452.09, 4.33);
  graph->SetPoint( 6, 509.11, 3.34);
  graph->SetPoint( 7, 562.56, 2.80);
  graph->SetPoint( 8, 587.96, 2.43);
  graph->SetPoint( 9, 613.80, 2.11);
  graph->SetPoint(10, 641.87, 1.85);
  graph->SetPoint(11, 652.56, 1.80);
  graph->SetPoint(12, 683.76, 1.46);
  graph->SetPoint(13, 744.36, 1.00);
  return graph;
}
