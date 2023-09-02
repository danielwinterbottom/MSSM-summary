#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 240.68, 3.18);
  graph->SetPoint( 1, 270.03, 5.73);
  graph->SetPoint( 2, 286.75, 5.85);
  graph->SetPoint( 3, 329.07, 5.63);
  graph->SetPoint( 4, 373.09, 5.45);
  graph->SetPoint( 5, 399.70, 5.47);
  graph->SetPoint( 6, 411.65, 5.35);
  graph->SetPoint( 7, 457.03, 4.56);
  graph->SetPoint( 8, 507.20, 3.46);
  graph->SetPoint( 9, 543.71, 2.97);
  graph->SetPoint(10, 551.56, 2.92);
  graph->SetPoint(11, 569.30, 2.56);
  graph->SetPoint(12, 606.16, 1.95);
  graph->SetPoint(13, 626.97, 1.72);
  graph->SetPoint(14, 648.13, 1.29);
  graph->SetPoint(15, 656.32, 1.10);
  if(filled){
    graph->SetPoint(16, 656.32, 1.00);
    graph->SetPoint(17, 240.68, 1.00);
    graph->SetPoint(18, 240.68, 3.18);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 240.68, 3.18);
  graph->SetPoint( 1, 270.03, 5.73);
  graph->SetPoint( 2, 286.75, 5.85);
  graph->SetPoint( 3, 329.07, 5.63);
  graph->SetPoint( 4, 373.09, 5.45);
  graph->SetPoint( 5, 399.70, 5.47);
  graph->SetPoint( 6, 411.65, 5.35);
  graph->SetPoint( 7, 457.03, 4.56);
  graph->SetPoint( 8, 507.20, 3.46);
  graph->SetPoint( 9, 543.71, 2.97);
  graph->SetPoint(10, 551.56, 2.92);
  graph->SetPoint(11, 569.30, 2.56);
  graph->SetPoint(12, 606.16, 1.95);
  graph->SetPoint(13, 626.97, 1.72);
  graph->SetPoint(14, 648.13, 1.29);
  graph->SetPoint(15, 656.32, 1.10);
  return graph;
}
