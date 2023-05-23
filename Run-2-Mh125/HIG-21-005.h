/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_21_005_obs(bool filled){
  // Function to return the observed cotour. Call with filled=true/false. 
  //
  // true  : use for a TGraph that should be plotted as filled
  // false : use for a TGraph that should be plotted as NOT filled 
  // 
  // Add the x-value in the column of second arguments; add the y-valuess in 
  // the column of third arguments to TGraph::SetPoint(*, *, *).
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 242.59, 3.32);
  graph->SetPoint( 1, 247.55, 2.37);
  graph->SetPoint( 2, 253.93, 1.93);
  graph->SetPoint( 3, 264.16, 1.89);
  graph->SetPoint( 4, 288.74, 2.26);
  graph->SetPoint( 5, 306.70, 1.92);
  graph->SetPoint( 6, 337.35, 1.91);
  graph->SetPoint( 7, 430.61, 1.13);
  if(filled){
    // In case of filled=true add three points here to make sure the filled 
    // contour is closed and convex. 
    graph->SetPoint( 8, 430.61, 0.90);
    graph->SetPoint( 9, 242.59, 0.90);
    graph->SetPoint(10, 242.59, 3.32);
  }
  return graph;
}

TGraph* HIG_21_005_exp(){
  // Function to return the expected cotour. These contours are not supposed to  
  // be filled. 
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 245.93, 4.50);
  graph->SetPoint( 1, 253.02, 3.33);
  graph->SetPoint( 2, 260.70, 2.75);
  graph->SetPoint( 3, 268.63, 2.37);
  graph->SetPoint( 4, 288.48, 2.23);
  graph->SetPoint( 5, 310.10, 2.35);
  graph->SetPoint( 6, 342.36, 2.62);
  graph->SetPoint( 7, 376.65, 1.19);
  return graph;
}
