/* This can be used as a template for setting up inputs for MSSM_limits_*.C */

#include "TGraph.h"

TGraph* HIG_18_023_obs(bool filled){
  // Function to return the observed cotour. Call with filled=true/false. 
  //
  // true  : use for a TGraph that should be plotted as filled
  // false : use for a TGraph that should be plotted as NOT filled 
  // 
  // Add the x-value in the column of second arguments; add the y-valuess in 
  // the column of third arguments to TGraph::SetPoint(*, *, *).
  TGraph* graph = new TGraph();
  //graph->SetPoint( 0, 220.00, 1.76);
  graph->SetPoint( 0, 239.99, 1.81); //2.26
  graph->SetPoint( 1, 259.87, 2.37); //3.01
  graph->SetPoint( 2, 280.07, 2.88); //3.51
  graph->SetPoint( 3, 299.95, 3.15); //4.00
  graph->SetPoint( 4, 320.05, 3.09); //3.76
  graph->SetPoint( 5, 339.71, 3.06); //3.76
  //graph->SetPoint( 7, 347.52, 1.00);
  if(filled){
    // In case of filled=true add three points here to make sure the filled 
    // contour is closed and convex. 
    graph->SetPoint( 6, 339.71, 1.00);
    graph->SetPoint( 7, 239.99, 1.00);
    graph->SetPoint( 8, 239.99, 1.81);
  }
  return graph;
}

TGraph* HIG_18_023_exp(){
  // Function to return the expected cotour. These contours are not supposed to  
  // be filled. 
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 220.00, 1.55); //1.76
  graph->SetPoint( 1, 239.99, 2.13); //2.76
  graph->SetPoint( 2, 259.87, 2.36); //3.00
  graph->SetPoint( 3, 280.07, 2.48); //3.25
  graph->SetPoint( 4, 299.95, 2.63); //3.26
  graph->SetPoint( 5, 320.05, 2.79); //3.51
  graph->SetPoint( 6, 339.72, 3.14); //3.76
  //graph->SetPoint( 7, 347.52, 1.00);
  return graph;
}
