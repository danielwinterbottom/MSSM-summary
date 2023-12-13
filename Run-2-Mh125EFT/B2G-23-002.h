#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.70, 6.28);
  graph->SetPoint( 1, 267.35, 6.60);
  graph->SetPoint( 2, 278.65, 6.89);
  graph->SetPoint( 3, 298.76, 6.91);
  graph->SetPoint( 4, 317.37, 6.93);
  graph->SetPoint( 5, 348.26, 5.36);
  graph->SetPoint( 6, 398.86, 5.60);
  graph->SetPoint( 7, 450.74, 5.04);
  graph->SetPoint( 8, 497.99, 3.90);
  graph->SetPoint( 9, 545.25, 2.81);
  graph->SetPoint(10, 596.01, 2.43);
  if(filled){
    graph->SetPoint(11, 596.01, 1.00);
    graph->SetPoint(12, 257.70, 1.00);
    graph->SetPoint(13, 257.70, 6.28);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 258.11, 6.56);
  graph->SetPoint( 1, 267.35, 6.60);
  graph->SetPoint( 2, 278.26, 6.39);
  graph->SetPoint( 3, 298.13, 5.91);
  graph->SetPoint( 4, 316.87, 5.74);
  graph->SetPoint( 5, 348.45, 5.59);
  graph->SetPoint( 6, 398.33, 4.91);
  graph->SetPoint( 7, 449.77, 4.07);
  graph->SetPoint( 8, 496.96, 3.29);
  graph->SetPoint( 9, 544.61, 2.61);
  graph->SetPoint(10, 595.16, 2.22);
  return graph;
}
