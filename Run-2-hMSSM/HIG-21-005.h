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
  graph->SetPoint( 0, 251.97, 1.71);
  graph->SetPoint( 1, 286.11, 2.33);
  graph->SetPoint( 2, 303.23, 1.99);
  graph->SetPoint( 3, 336.36, 2.08);
  graph->SetPoint( 4, 383.58, 1.75);
  graph->SetPoint( 5, 414.22, 1.90);
  graph->SetPoint( 6, 440.65, 2.10);
  graph->SetPoint( 7, 490.53, 1.95);
  if(filled){
    // In case of filled=true add three points here to make sure the filled 
    // contour is closed and convex. 
    graph->SetPoint( 8, 490.53, 0.90);
    graph->SetPoint( 9, 251.97, 0.90);
    graph->SetPoint(10, 251.97, 1.71);
  }
  return graph;
}

TGraph* HIG_21_005_exp(){
  // Function to return the expected cotour. These contours are not supposed to  
  // be filled. 
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 234.19, 2.58);
  graph->SetPoint( 1, 249.36, 3.03);
  graph->SetPoint( 2, 257.29, 2.67);
  graph->SetPoint( 3, 264.78, 2.36);
  graph->SetPoint( 4, 285.73, 2.29);
  graph->SetPoint( 5, 308.48, 2.45);
  graph->SetPoint( 6, 341.96, 2.79);
  graph->SetPoint( 7, 387.83, 2.11);
  graph->SetPoint( 8, 414.76, 1.95);
  graph->SetPoint( 9, 438.75, 1.89);
  graph->SetPoint(10, 486.30, 1.56);
  graph->SetPoint(11, 532.20, 1.23);
  return graph;
}
