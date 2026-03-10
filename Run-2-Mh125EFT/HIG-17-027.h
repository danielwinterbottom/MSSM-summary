/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_17_027_obs(bool filled){
  // Function to return the observed cotour. Call with filled=true/false. 
  //
  // true  : use for a TGraph that should be plotted as filled
  // false : use for a TGraph that should be plotted as NOT filled 
  // 
  // Add the x-value in the column of second arguments; add the y-valuess in 
  // the column of third arguments to TGraph::SetPoint(*, *, *).
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 400.00, 1.03);
  graph->SetPoint( 1, 409.90, 1.23);
  graph->SetPoint( 2, 430.12, 1.27);
  graph->SetPoint( 3, 439.82, 1.39);
  graph->SetPoint( 4, 459.83, 1.52);
  graph->SetPoint( 5, 489.95, 1.58);
  graph->SetPoint( 6, 499.86, 1.71);
  graph->SetPoint( 7, 509.97, 1.96);
  graph->SetPoint( 8, 519.87, 1.97);
  graph->SetPoint( 9, 529.98, 1.76);
  graph->SetPoint(10, 539.89, 1.65);
  graph->SetPoint(11, 550.0 , 1.43);
  graph->SetPoint(12, 559.90, 1.31);
  graph->SetPoint(13, 579.91, 1.33);
  graph->SetPoint(14, 590.02, 1.22);
  graph->SetPoint(15, 609.83, 1.46);
  graph->SetPoint(16, 619.94, 1.72);
  graph->SetPoint(17, 630.05, 1.73);
  graph->SetPoint(18, 639.95, 1.86);
  graph->SetPoint(19, 659.97, 1.87);
  graph->SetPoint(20, 669.87, 1.99);
  graph->SetPoint(21, 679.98, 1.89);
  graph->SetPoint(22, 700.00, 1.90);
  if(filled){
    // In case of filled=true add three points here to make sure the filled 
    // contour is closed and convex. 
    graph->SetPoint(23,700.00, 1.00);
    graph->SetPoint(24,400.00, 1.00);
    graph->SetPoint(25,400.00, 1.03);
  }
  return graph;
}

TGraph* HIG_17_027_exp(){
  // Function to return the expected cotour. These contours are not supposed to  
  // be filled. 
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 400.00, 2.18);
  graph->SetPoint( 1, 410.31, 2.35);
  graph->SetPoint( 2, 429.71, 2.28);
  graph->SetPoint( 3, 439.82, 2.32);
  graph->SetPoint( 4, 469.94, 2.11);
  graph->SetPoint( 5, 479.84, 2.13);
  graph->SetPoint( 6, 489.95, 2.04);
  graph->SetPoint( 7, 509.97, 2.08);
  graph->SetPoint( 8, 529.98, 1.88);
  graph->SetPoint( 9, 539.47, 1.89);
  graph->SetPoint(10, 559.90, 1.67);
  graph->SetPoint(11, 569.60, 1.68);
  graph->SetPoint(12, 588.99, 1.46);
  graph->SetPoint(13, 610.24, 1.46);
  graph->SetPoint(14, 621.18, 1.36);
  graph->SetPoint(15, 630.05, 1.36);
  graph->SetPoint(16, 639.95, 1.24);
  graph->SetPoint(17, 651.30, 1.23);
  graph->SetPoint(18, 659.97, 1.13);
  graph->SetPoint(19, 680.39, 1.14);
  graph->SetPoint(20, 690.09, 1.00);
  graph->SetPoint(21, 700.00, 1.00);
  return graph;
}
