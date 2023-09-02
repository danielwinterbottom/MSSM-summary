/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_18_005_obs(bool filled){
  // Function to return the observed cotour. Call with filled=true/false. 
  //
  // true  : use for a TGraph that should be plotted as filled
  // false : use for a TGraph that should be plotted as NOT filled 
  // 
  // Add the x-value in the column of second arguments; add the y-valuess in 
  // the column of third arguments to TGraph::SetPoint(*, *, *).
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 223.29, 2.11);
  graph->SetPoint( 1, 233.54, 2.95);
  graph->SetPoint( 2, 238.30, 2.98);
  graph->SetPoint( 3, 243.42, 2.75);
  graph->SetPoint( 4, 248.18, 2.71);
  graph->SetPoint( 5, 253.67, 2.90);
  graph->SetPoint( 6, 263.19, 2.90);
  graph->SetPoint( 7, 273.43, 2.95);
  graph->SetPoint( 8, 281.12, 2.91);
  graph->SetPoint( 9, 295.76, 3.34);
  graph->SetPoint(10, 308.57, 3.77);
  graph->SetPoint(11, 318.09, 3.81);
  graph->SetPoint(12, 328.70, 3.47);
  graph->SetPoint(13, 338.59, 3.54);
  graph->SetPoint(14, 348.47, 3.09);
  graph->SetPoint(15, 358.72, 2.20);
  if(filled){
    // In case of filled=true add three points here to make sure the filled 
    // contour is closed and convex. 
    graph->SetPoint(16, 358.72, 1.00);
    graph->SetPoint(17, 223.29, 1.00);
    graph->SetPoint(18, 223.29, 2.11);
  }
  return graph;
}

TGraph* HIG_18_005_exp(){
  // Function to return the expected cotour. These contours are not supposed to  
  // be filled. 
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 223.29, 2.23);
  graph->SetPoint( 1, 233.54, 2.63);
  graph->SetPoint( 2, 238.30, 2.73);
  graph->SetPoint( 3, 243.42, 2.83);
  graph->SetPoint( 4, 248.18, 2.88);
  graph->SetPoint( 5, 253.67, 2.93);
  graph->SetPoint( 6, 263.19, 3.05);
  graph->SetPoint( 7, 273.43, 3.12);
  graph->SetPoint( 8, 281.12, 3.19);
  graph->SetPoint( 9, 295.76, 3.34);
  graph->SetPoint(10, 308.57, 3.46);
  graph->SetPoint(11, 318.09, 3.53);
  graph->SetPoint(12, 328.70, 3.68);
  graph->SetPoint(13, 338.59, 3.86);
  graph->SetPoint(14, 348.47, 2.98);
  graph->SetPoint(15, 358.72, 1.81);
  graph->SetPoint(16, 378.85, 1.36);
  return graph;
}
