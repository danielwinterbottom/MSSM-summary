#include "TGraph.h"

TGraph* HIG_17_033_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0, 195.93, 6.54);
  graph->SetPoint(  1, 205.06, 5.80);
  graph->SetPoint(  2, 212.22, 5.25);
  graph->SetPoint(  3, 219.33, 4.77);
  graph->SetPoint(  4, 226.36, 4.35);
  graph->SetPoint(  5, 233.26, 3.96);
  graph->SetPoint(  6, 240.40, 3.29);
  if(filled){
    graph->SetPoint( 7, 240.40, 1.00);
    graph->SetPoint( 8, 195.93, 1.00);
    graph->SetPoint( 9, 195.93, 6.54);
  }
  return graph;
}

TGraph* HIG_17_033_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0, 194.24, 5.50);
  graph->SetPoint(  1, 218.03, 4.32);
  graph->SetPoint(  2, 240.40, 3.29);
  return graph;
}
