/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_21_011_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 256.82, 5.56);
  graph->SetPoint( 1, 277.42, 5.84);
  graph->SetPoint( 2, 297.79, 6.22);
  graph->SetPoint( 3, 317.88, 5.86);
  graph->SetPoint( 4, 347.34, 4.91);
  graph->SetPoint( 5, 446.30, 3.52);
  graph->SetPoint( 6, 527.22, 1.04);
  if(filled){
    graph->SetPoint(7, 527.22, 0.40);
    graph->SetPoint(8, 256.82, 0.40);
    graph->SetPoint(9, 256.82, 5.56);
  }
  return graph;
}

TGraph* HIG_21_011_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.10, 5.82);
  graph->SetPoint( 1, 277.36, 5.76);
  graph->SetPoint( 2, 297.28, 5.39);
  graph->SetPoint( 3, 317.36, 5.24);
  graph->SetPoint( 4, 347.67, 5.25);
  graph->SetPoint( 5, 445.36, 3.12);
  graph->SetPoint( 6, 535.03, 1.38);
  return graph;
}
