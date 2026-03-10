#include "TGraph.h"

TGraph* HIG_22_004_obs(bool filled){
  TGraph* graph = new TGraph();

  graph->SetPoint(0, 225, 2.54);
  graph->SetPoint(1, 250, 3.12);
  graph->SetPoint(2, 275, 3.40);
  graph->SetPoint(3, 300, 4.01);
  graph->SetPoint(4, 325, 4.02);
  graph->SetPoint(5, 350, 2.17);
  graph->SetPoint(6, 375, 1.43);
  graph->SetPoint(7, 400, 0.75);

  if(filled){
    graph->SetPoint( 8, 225.00, 1.00);
    graph->SetPoint( 9, 225.00, 2.54);
  }

  return graph;
}

TGraph* HIG_22_004_exp(){
  TGraph* graph = new TGraph();

  graph->SetPoint(0, 225, 2.60);
  graph->SetPoint(1, 250, 3.34);
  graph->SetPoint(2, 275, 3.56);
  graph->SetPoint(3, 300, 3.65);
  graph->SetPoint(4, 325, 3.90);
  graph->SetPoint(5, 350, 2.53);
  graph->SetPoint(6, 375, 1.47);
  graph->SetPoint(7, 400, 0.95);


  return graph;
}




























