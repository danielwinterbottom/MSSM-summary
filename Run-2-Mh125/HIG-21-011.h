/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_21_011_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 258.12, 6.11);
  graph->SetPoint( 1, 278.32, 6.11);
  graph->SetPoint( 2, 298.63, 6.37);
  graph->SetPoint( 3, 317.47, 5.99);
  graph->SetPoint( 4, 347.86, 4.91);
  graph->SetPoint( 5, 446.63, 3.35);
  if(filled){
    graph->SetPoint(6, 446.63, 0.40);
    graph->SetPoint(7, 258.12, 0.40);
    graph->SetPoint(8, 258.12, 6.11);
  }
  return graph;
}

TGraph* HIG_21_011_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 258.33, 6.41);
  graph->SetPoint( 1, 278.26, 6.01);
  graph->SetPoint( 2, 298.05, 5.52);
  graph->SetPoint( 3, 317.11, 5.31);
  graph->SetPoint( 4, 348.19, 5.29);
  graph->SetPoint( 5, 445.44, 2.85);
  return graph;
}
