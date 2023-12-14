#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 256.99, 5.72);
  graph->SetPoint( 1, 267.42, 6.07);
  graph->SetPoint( 2, 277.81, 6.55);
  graph->SetPoint( 3, 287.94, 6.58);
  graph->SetPoint( 4, 298.07, 6.62);
  graph->SetPoint( 5, 308.17, 6.63);
  graph->SetPoint( 6, 318.27, 6.67);
  graph->SetPoint( 7, 327.98, 5.87);
  graph->SetPoint( 8, 337.74, 5.43);
  graph->SetPoint( 9, 347.53, 5.09);
  graph->SetPoint(10, 357.57, 5.05);
  graph->SetPoint(11, 367.60, 4.99);
  graph->SetPoint(12, 377.66, 4.97);
  graph->SetPoint(13, 387.77, 5.01);
  graph->SetPoint(14, 398.00, 5.21);
  graph->SetPoint(15, 407.91, 5.03);
  graph->SetPoint(16, 417.86, 4.88);
  graph->SetPoint(17, 427.81, 4.76);
  graph->SetPoint(18, 437.79, 4.67);
  graph->SetPoint(19, 447.80, 4.62);
  graph->SetPoint(20, 457.59, 4.35);
  graph->SetPoint(21, 467.34, 4.08);
  graph->SetPoint(22, 477.07, 3.83);
  graph->SetPoint(23, 486.74, 3.58);
  graph->SetPoint(24, 496.41, 3.35);
  graph->SetPoint(25, 505.87, 3.07);
  graph->SetPoint(26, 515.29, 2.83);
  graph->SetPoint(27, 524.55, 2.58);
  graph->SetPoint(28, 533.75, 2.36);
  graph->SetPoint(29, 542.77, 2.15);
  graph->SetPoint(30, 552.19, 2.03);
  graph->SetPoint(31, 561.74, 1.94);
  graph->SetPoint(32, 571.39, 1.87);
  graph->SetPoint(33, 581.06, 1.81);
  graph->SetPoint(34, 590.77, 1.76);
  graph->SetPoint(35, 599.21, 1.58);
  graph->SetPoint(36, 607.46, 1.42);
  graph->SetPoint(37, 615.45, 1.27);
  graph->SetPoint(38, 622.57, 1.10);
  if(filled){
    graph->SetPoint(39, 622.57, 1.00);
    graph->SetPoint(40, 256.99, 1.00);
    graph->SetPoint(41, 256.99, 5.72);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.20, 5.93);
  graph->SetPoint( 1, 267.42, 6.10);
  graph->SetPoint( 2, 277.48, 5.90);
  graph->SetPoint( 3, 287.45, 5.71);
  graph->SetPoint( 4, 297.37, 5.49);
  graph->SetPoint( 5, 307.44, 5.44);
  graph->SetPoint( 6, 317.51, 5.40);
  graph->SetPoint( 7, 327.58, 5.35);
  graph->SetPoint( 8, 337.66, 5.34);
  graph->SetPoint( 9, 347.74, 5.34);
  graph->SetPoint(10, 357.72, 5.22);
  graph->SetPoint(11, 367.64, 5.03);
  graph->SetPoint(12, 377.55, 4.85);
  graph->SetPoint(13, 387.45, 4.67);
  graph->SetPoint(14, 397.33, 4.49);
  graph->SetPoint(15, 407.16, 4.28);
  graph->SetPoint(16, 416.95, 4.07);
  graph->SetPoint(17, 426.77, 3.89);
  graph->SetPoint(18, 436.60, 3.73);
  graph->SetPoint(19, 446.43, 3.59);
  graph->SetPoint(20, 456.11, 3.38);
  graph->SetPoint(21, 465.76, 3.18);
  graph->SetPoint(22, 475.33, 2.99);
  graph->SetPoint(23, 485.00, 2.84);
  graph->SetPoint(24, 494.62, 2.69);
  graph->SetPoint(25, 503.96, 2.50);
  graph->SetPoint(26, 513.43, 2.35);
  graph->SetPoint(27, 522.79, 2.20);
  graph->SetPoint(28, 531.97, 2.05);
  graph->SetPoint(29, 541.24, 1.92);
  graph->SetPoint(30, 550.60, 1.82);
  graph->SetPoint(31, 559.88, 1.72);
  graph->SetPoint(32, 569.07, 1.62);
  graph->SetPoint(33, 578.19, 1.53);
  graph->SetPoint(34, 587.52, 1.46);
  graph->SetPoint(35, 596.02, 1.33);
  graph->SetPoint(36, 604.07, 1.21);
  graph->SetPoint(37, 611.37, 1.07);  
  return graph;
}
