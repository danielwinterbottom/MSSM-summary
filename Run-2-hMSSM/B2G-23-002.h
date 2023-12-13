#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.55, 5.71);
  graph->SetPoint( 1, 267.06, 6.02);
  graph->SetPoint( 2, 278.45, 6.53);
  graph->SetPoint( 3, 298.63, 6.59);
  graph->SetPoint( 4, 318.33, 6.65);
  graph->SetPoint( 5, 348.22, 5.07);
  graph->SetPoint( 6, 398.69, 5.16);
  graph->SetPoint( 7, 450.39, 4.51);
  graph->SetPoint( 8, 497.10, 3.32);
  graph->SetPoint( 9, 542.46, 2.14);
  graph->SetPoint(10, 591.63, 1.71);
  if(filled){
    graph->SetPoint(11, 591.63, 1.00);
    graph->SetPoint(12, 257.55, 1.00);
    graph->SetPoint(13, 257.55, 5.71);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.79, 5.95);
  graph->SetPoint( 1, 267.06, 6.02);
  graph->SetPoint( 2, 278.12, 5.87);
  graph->SetPoint( 3, 297.95, 5.49);
  graph->SetPoint( 4, 317.57, 5.38);
  graph->SetPoint( 5, 348.43, 5.30);
  graph->SetPoint( 6, 398.00, 4.44);
  graph->SetPoint( 7, 448.94, 3.49);
  graph->SetPoint( 8, 495.25, 2.66);
  graph->SetPoint( 9, 540.97, 1.92);
  graph->SetPoint(10, 588.21, 1.41);
  return graph;
}
