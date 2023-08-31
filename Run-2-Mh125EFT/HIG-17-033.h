#include "TGraph.h"

TGraph* HIG_17_033_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0, 128.12, 9.12);
  graph->SetPoint(  1, 151.09, 7.36);
  graph->SetPoint(  2, 154.96, 7.38);
  graph->SetPoint(  3, 160.87, 8.84);
  graph->SetPoint(  4, 165.02, 9.32);
  graph->SetPoint(  5, 174.83, 9.55);
  graph->SetPoint(  6, 177.06, 6.49);
  graph->SetPoint(  7, 184.92, 6.30);
  graph->SetPoint(  8, 194.93, 6.28);
  graph->SetPoint(  9, 196.17, 5.40);
  graph->SetPoint( 10, 206.94, 4.88);
  graph->SetPoint( 11, 209.12, 4.33);
  graph->SetPoint( 12, 224.94, 3.51);
  graph->SetPoint( 13, 234.98, 3.50);
  graph->SetPoint( 14, 242.47, 2.98);
  graph->SetPoint( 15, 237.60, 1.66);
  graph->SetPoint( 16, 246.04, 1.48);
  graph->SetPoint( 17, 262.79, 1.84);
  graph->SetPoint( 18, 301.04, 2.48);
  graph->SetPoint( 19, 311.61, 2.83);
  graph->SetPoint( 20, 322.71, 3.02);
  graph->SetPoint( 21, 333.53, 3.31);
  graph->SetPoint( 22, 343.62, 3.39);
  graph->SetPoint( 23, 362.92, 3.16);
  graph->SetPoint( 24, 391.59, 2.21);
  graph->SetPoint( 25, 405.81, 1.60);
  if(filled){
    graph->SetPoint(26, 405.81, 1.00);
    graph->SetPoint(27, 128.12, 1.00);
    graph->SetPoint(28, 128.12, 9.12);
  }
  return graph;
}

TGraph* HIG_17_033_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0, 128.12, 8.21);
  graph->SetPoint(  1, 135.97, 7.89);
  graph->SetPoint(  2, 152.68, 7.15);
  graph->SetPoint(  3, 164.06, 8.00);
  graph->SetPoint(  4, 173.85, 7.89);
  graph->SetPoint(  5, 183.66, 7.16);
  graph->SetPoint(  6, 196.91, 6.35);
  graph->SetPoint(  7, 208.17, 5.66);
  graph->SetPoint(  8, 226.77, 4.89);
  graph->SetPoint(  9, 235.57, 4.62);
  graph->SetPoint( 10, 244.47, 4.04);
  graph->SetPoint( 11, 253.36, 3.10);
  graph->SetPoint( 12, 262.20, 2.51);
  graph->SetPoint( 13, 269.00, 2.41);
  graph->SetPoint( 14, 280.51, 2.38);
  graph->SetPoint( 15, 300.35, 2.40);
  graph->SetPoint( 16, 309.57, 2.44);
  graph->SetPoint( 17, 318.93, 2.52);
  graph->SetPoint( 18, 332.82, 2.82);
  graph->SetPoint( 19, 344.38, 2.73);
  graph->SetPoint( 20, 374.11, 2.01);
  graph->SetPoint( 21, 389.18, 1.45);
  graph->SetPoint( 22, 405.81, 1.17);
  return graph;
}
