#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.18, 6.31);
  graph->SetPoint( 1, 267.48, 6.40);
  graph->SetPoint( 2, 277.44, 6.29);
  graph->SetPoint( 3, 397.71, 5.03);
  graph->SetPoint( 4, 496.63, 3.51);
  graph->SetPoint( 5, 594.78, 2.43);
  graph->SetPoint( 6, 692.09, 1.67);
  if(filled){
    graph->SetPoint( 7, 692.09, 1.00);
    graph->SetPoint( 8, 257.18, 1.00);
    graph->SetPoint( 9, 257.18, 6.31);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.18, 6.31);
  graph->SetPoint( 1, 267.48, 6.40);
  graph->SetPoint( 2, 277.44, 6.29);
  graph->SetPoint( 3, 397.71, 5.03);
  graph->SetPoint( 4, 496.63, 3.51);
  graph->SetPoint( 5, 594.78, 2.43);
  graph->SetPoint( 6, 692.09, 1.67);
  return graph;
}
