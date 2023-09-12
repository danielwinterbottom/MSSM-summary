#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 200.204, 3.300);
  graph->SetPoint( 1, 217.036, 6.304);
  graph->SetPoint( 2, 227.017, 6.400);
  graph->SetPoint( 3, 257.420, 6.022);
  graph->SetPoint( 4, 286.575, 5.789);
  graph->SetPoint( 5, 309.085, 5.789);
  graph->SetPoint( 6, 371.499, 4.827);
  graph->SetPoint( 7, 413.575, 4.055);
  graph->SetPoint( 8, 456.668, 3.585);
  graph->SetPoint( 9, 468.484, 3.508);
  graph->SetPoint(10, 513.086, 2.932);
  graph->SetPoint(11, 567.127, 2.479);
  graph->SetPoint(12, 578.245, 2.436);
  graph->SetPoint(13, 633.298, 1.972);
  graph->SetPoint(14, 712.266, 1.539);
  if(filled){
    graph->SetPoint(15, 712.226, 1.00);
    graph->SetPoint(16, 200.204, 1.00);
    graph->SetPoint(17, 200.204, 3.30);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 200.204, 3.300);
  graph->SetPoint( 1, 217.036, 6.304);
  graph->SetPoint( 2, 227.017, 6.400);
  graph->SetPoint( 3, 257.420, 6.022);
  graph->SetPoint( 4, 286.575, 5.789);
  graph->SetPoint( 5, 309.085, 5.789);
  graph->SetPoint( 6, 371.499, 4.827);
  graph->SetPoint( 7, 413.575, 4.055);
  graph->SetPoint( 8, 456.668, 3.585);
  graph->SetPoint( 9, 468.484, 3.508);
  graph->SetPoint(10, 513.086, 2.932);
  graph->SetPoint(11, 567.127, 2.479);
  graph->SetPoint(12, 578.245, 2.436);
  graph->SetPoint(13, 633.298, 1.972);
  graph->SetPoint(14, 712.266, 1.539);
  return graph;
}
