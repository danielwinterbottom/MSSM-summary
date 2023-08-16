#include "TGraph.h"

TGraph* HIG_21_001_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0, 344.90,  1.00);
  graph->SetPoint(  1, 349.24,  1.54);
  graph->SetPoint(  2, 388.29,  2.21);
  graph->SetPoint(  3, 418.66,  2.95);
  graph->SetPoint(  4, 445.55,  4.11);
  graph->SetPoint(  5, 476.79,  4.95);
  graph->SetPoint(  6, 504.55,  5.75);
  graph->SetPoint(  7, 526.25,  6.13);
  graph->SetPoint(  8, 567.90,  6.52);
  graph->SetPoint(  9, 614.75,  7.18);  
  graph->SetPoint( 10, 655.53,  7.45);  
  graph->SetPoint( 11, 699.78,  7.72);  
  graph->SetPoint( 12, 750.98,  8.25);  
  graph->SetPoint( 13, 793.49,  8.52);  
  graph->SetPoint( 14, 831.67,  9.17);  
  graph->SetPoint( 15, 869.85,  9.66);  
  graph->SetPoint( 16, 878.53, 10.00);  
  if(filled){
    graph->SetPoint(17,   90.00, 10.00);
    graph->SetPoint(18,   90.00,  1.00);
    graph->SetPoint(19,  344.90,  1.00);
  }
  return graph;
}

TGraph* HIG_21_001_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint(  0,  344.90, 1.00);
  graph->SetPoint(  1,  345.77, 2.15);
  graph->SetPoint(  2,  349.24, 2.55);
  graph->SetPoint(  3,  360.52, 2.98);
  graph->SetPoint(  4,  400.43, 3.78);
  graph->SetPoint(  5,  446.42, 4.65);
  graph->SetPoint(  6,  494.14, 5.24);
  graph->SetPoint(  7,  534.92, 5.87);
  graph->SetPoint(  8,  565.29, 6.39);
  graph->SetPoint(  9,  599.13, 6.61);  
  graph->SetPoint( 10,  625.16, 6.97);  
  graph->SetPoint( 11,  700.65, 7.55);  
  graph->SetPoint( 12,  753.58, 7.91);  
  graph->SetPoint( 13,  850.76, 8.49);  
  graph->SetPoint( 14,  954.01, 9.12);  
  graph->SetPoint( 15,  995.66, 9.35);  
  graph->SetPoint( 16, 1033.84, 9.91);  
  return graph;
}
