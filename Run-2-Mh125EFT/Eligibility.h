#include "TGraph.h"

TGraph* Eligibility(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 172.23,  1.00);
  graph->SetPoint( 1, 206.94,  1.23);
  graph->SetPoint( 2, 216.49,  1.52);
  graph->SetPoint( 3, 191.32,  1.97);
  graph->SetPoint( 4, 166.16,  2.47);
  graph->SetPoint( 5, 150.54,  3.07);
  graph->SetPoint( 6, 137.53,  4.12);
  graph->SetPoint( 7, 130.59,  5.39);
  graph->SetPoint( 8, 127.11,  6.94);
  graph->SetPoint( 9, 125.38,  8.64);
  graph->SetPoint(10, 124.51, 10.00);
  graph->SetPoint(11,  90.00, 10.00);
  graph->SetPoint(12,  90.00,  1.00);
  graph->SetPoint(13, 172.23,  1.00);
  return graph;
}
