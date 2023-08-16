#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 258.23, 7.79);
  graph->SetPoint( 1, 268.37, 7.91);
  graph->SetPoint( 2, 278.40, 7.75);
  graph->SetPoint( 3, 398.37, 6.22);
  graph->SetPoint( 4, 498.03, 4.67);
  graph->SetPoint( 5, 597.03, 3.32);
  graph->SetPoint( 6, 695.17, 2.27);
  graph->SetPoint( 7, 793.93, 1.77);
  if(filled){
    graph->SetPoint( 8, 793.93, 1.00);
    graph->SetPoint( 9, 258.23, 1.00);
    graph->SetPoint(10, 258.23, 7.79);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 258.23, 7.79);
  graph->SetPoint( 1, 268.37, 7.91);
  graph->SetPoint( 2, 278.40, 7.75);
  graph->SetPoint( 3, 398.37, 6.22);
  graph->SetPoint( 4, 498.03, 4.67);
  graph->SetPoint( 5, 597.03, 3.32);
  graph->SetPoint( 6, 695.17, 2.27);
  graph->SetPoint( 7, 793.93, 1.77);
  return graph;
}
