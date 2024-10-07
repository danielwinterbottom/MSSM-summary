#include "TGraph.h"

TGraph* HIG_20_016_obs(bool filled){
  TGraph* graph = new TGraph();


  graph->SetPoint(graph->GetN(), 135.81, 10.10);
  graph->SetPoint(graph->GetN(), 138.16, 9.70);
  graph->SetPoint(graph->GetN(), 144.42, 9.32);
  graph->SetPoint(graph->GetN(), 154.60, 9.16);
  graph->SetPoint(graph->GetN(), 160.08, 9.49);
  graph->SetPoint(graph->GetN(), 163.21, 9.88);
  graph->SetPoint(graph->GetN(), 165.56, 10.11);
  graph->SetPoint(graph->GetN(), 167.91, 9.62);
  graph->SetPoint(graph->GetN(), 169.47, 9.04);
  graph->SetPoint(graph->GetN(), 175.73, 8.68);
  graph->SetPoint(graph->GetN(), 178.08, 8.34);
  graph->SetPoint(graph->GetN(), 179.65, 7.94);
  graph->SetPoint(graph->GetN(), 182.00, 7.70);
  graph->SetPoint(graph->GetN(), 191.39, 7.26);
  graph->SetPoint(graph->GetN(), 185.91, 7.17);
  graph->SetPoint(graph->GetN(), 178.86, 6.91);
  graph->SetPoint(graph->GetN(), 177.30, 6.79);
  graph->SetPoint(graph->GetN(), 185.13, 6.55);
  graph->SetPoint(graph->GetN(), 194.52, 6.73);
  graph->SetPoint(graph->GetN(), 196.09, 7.04);
  graph->SetPoint(graph->GetN(), 203.91, 6.76);
  graph->SetPoint(graph->GetN(), 218.79, 6.59);
  graph->SetPoint(graph->GetN(), 235.23, 6.53);
  graph->SetPoint(graph->GetN(), 248.53, 6.33);
  graph->SetPoint(graph->GetN(), 253.23, 5.97);
  graph->SetPoint(graph->GetN(), 257.14, 5.71);
  graph->SetPoint(graph->GetN(), 248.53, 5.44);
  graph->SetPoint(graph->GetN(), 248.53, 5.20);
  graph->SetPoint(graph->GetN(), 254.01, 5.04);
  graph->SetPoint(graph->GetN(), 263.41, 5.20);
  graph->SetPoint(graph->GetN(), 265.75, 5.39);
  graph->SetPoint(graph->GetN(), 278.28, 5.27);
  graph->SetPoint(graph->GetN(), 285.32, 5.25);
  graph->SetPoint(graph->GetN(), 304.11, 4.94);
  graph->SetPoint(graph->GetN(), 315.85, 4.78);
  graph->SetPoint(graph->GetN(), 337.77, 4.58);
  graph->SetPoint(graph->GetN(), 347.16, 4.42);
  graph->SetPoint(graph->GetN(), 358.12, 4.17);
  graph->SetPoint(graph->GetN(), 364.38, 3.90);
  graph->SetPoint(graph->GetN(), 375.34, 3.71);
  graph->SetPoint(graph->GetN(), 383.17, 3.41);
  graph->SetPoint(graph->GetN(), 395.69, 2.92);
  graph->SetPoint(graph->GetN(), 405.87, 2.68);
  graph->SetPoint(graph->GetN(), 413.70, 2.33);
  graph->SetPoint(graph->GetN(), 423.09, 2.15);
  graph->SetPoint(graph->GetN(), 429.35, 1.88);
  graph->SetPoint(graph->GetN(), 439.53, 1.60);
  graph->SetPoint(graph->GetN(), 445.01, 1.39);
  graph->SetPoint(graph->GetN(), 450.49, 1.25);
  graph->SetPoint(graph->GetN(), 457.53, 1.15);
  graph->SetPoint(graph->GetN(), 456.75, 1.00);
  

  if(filled){
    graph->SetPoint(graph->GetN(),  90,  1.00);
    graph->SetPoint(graph->GetN(),  90, 10.00);

  }
  return graph;
}

TGraph* HIG_20_016_exp(){
  TGraph* graph = new TGraph();

  graph->SetPoint(graph->GetN(), 184.34, 10.11);
  graph->SetPoint(graph->GetN(), 189.82, 9.00);
  graph->SetPoint(graph->GetN(), 196.09, 8.57);
  graph->SetPoint(graph->GetN(), 200.00, 7.94);
  graph->SetPoint(graph->GetN(), 206.26, 7.77);
  graph->SetPoint(graph->GetN(), 215.66, 7.07);
  graph->SetPoint(graph->GetN(), 225.05, 6.59);
  graph->SetPoint(graph->GetN(), 232.88, 6.47);
  graph->SetPoint(graph->GetN(), 239.14, 6.22);
  graph->SetPoint(graph->GetN(), 239.14, 5.97);
  graph->SetPoint(graph->GetN(), 246.18, 5.74);
  graph->SetPoint(graph->GetN(), 249.32, 5.41);
  graph->SetPoint(graph->GetN(), 264.97, 4.84);
  graph->SetPoint(graph->GetN(), 290.80, 4.41);
  graph->SetPoint(graph->GetN(), 324.46, 4.30);
  graph->SetPoint(graph->GetN(), 345.60, 4.24);
  graph->SetPoint(graph->GetN(), 356.56, 4.06);
  graph->SetPoint(graph->GetN(), 372.99, 3.61);
  graph->SetPoint(graph->GetN(), 388.65, 3.22);
  graph->SetPoint(graph->GetN(), 398.04, 2.92);
  graph->SetPoint(graph->GetN(), 407.44, 2.69);
  graph->SetPoint(graph->GetN(), 415.26, 2.41);
  graph->SetPoint(graph->GetN(), 430.14, 2.17);
  graph->SetPoint(graph->GetN(), 439.53, 1.94);
  graph->SetPoint(graph->GetN(), 447.36, 1.70);
  graph->SetPoint(graph->GetN(), 452.84, 1.53);
  graph->SetPoint(graph->GetN(), 462.23, 1.32);
  graph->SetPoint(graph->GetN(), 465.36, 1.27);
  graph->SetPoint(graph->GetN(), 477.10, 1.17);
  graph->SetPoint(graph->GetN(), 478.67, 1.13);
  graph->SetPoint(graph->GetN(), 478.67, 1.02);


  return graph;
}




























