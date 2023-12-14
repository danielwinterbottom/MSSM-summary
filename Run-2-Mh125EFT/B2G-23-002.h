#include "TGraph.h"

TGraph* B2G_23_002_obs(bool filled){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.15, 6.29);
  graph->SetPoint( 1, 267.72, 6.63);
  graph->SetPoint( 2, 278.01, 6.92);
  graph->SetPoint( 3, 288.11, 6.93);
  graph->SetPoint( 4, 298.20, 6.95);
  graph->SetPoint( 5, 308.26, 6.93);
  graph->SetPoint( 6, 317.33, 6.95);
  graph->SetPoint( 7, 327.84, 6.24);
  graph->SetPoint( 8, 337.76, 5.75);
  graph->SetPoint( 9, 347.56, 5.38);
  graph->SetPoint(10, 357.66, 5.38);
  graph->SetPoint(11, 367.74, 5.36);
  graph->SetPoint(12, 377.83, 5.37);
  graph->SetPoint(13, 387.96, 5.45);
  graph->SetPoint(14, 398.16, 5.65);
  graph->SetPoint(15, 408.12, 5.49);
  graph->SetPoint(16, 418.10, 5.37);
  graph->SetPoint(17, 428.09, 5.26);
  graph->SetPoint(18, 438.09, 5.18);
  graph->SetPoint(19, 448.12, 5.14);
  graph->SetPoint(20, 457.98, 4.88);
  graph->SetPoint(21, 467.83, 4.63);
  graph->SetPoint(22, 477.66, 4.39);
  graph->SetPoint(23, 487.48, 4.16);
  graph->SetPoint(24, 497.27, 3.93);
  graph->SetPoint(25, 507.00, 3.68);
  graph->SetPoint(26, 516.65, 3.43);
  graph->SetPoint(27, 526.33, 3.22);
  graph->SetPoint(28, 535.88, 2.98);
  graph->SetPoint(29, 545.53, 2.82);
  graph->SetPoint(30, 555.37, 2.73);
  graph->SetPoint(31, 565.18, 2.64);
  graph->SetPoint(32, 575.02, 2.56);
  graph->SetPoint(33, 584.90, 2.49);
  graph->SetPoint(34, 594.88, 2.46);
  graph->SetPoint(35, 604.56, 2.35);
  graph->SetPoint(36, 614.18, 2.22);
  graph->SetPoint(37, 623.64, 2.09);
  graph->SetPoint(38, 633.15, 1.97);
  graph->SetPoint(39, 642.82, 1.89);
  graph->SetPoint(40, 652.45, 1.81);
  graph->SetPoint(41, 661.98, 1.71);
  graph->SetPoint(42, 671.37, 1.61);
  graph->SetPoint(43, 680.71, 1.50);
  if(filled){
    graph->SetPoint(44, 680.71, 1.00);
    graph->SetPoint(45, 257.15, 1.00);
    graph->SetPoint(46, 257.15, 6.29);
  }
  return graph;
}

TGraph* B2G_23_002_exp(){
  TGraph* graph = new TGraph();
  graph->SetPoint( 0, 257.52, 6.53);
  graph->SetPoint( 1, 267.73, 6.65);
  graph->SetPoint( 2, 277.65, 6.43);
  graph->SetPoint( 3, 287.51, 6.18);
  graph->SetPoint( 4, 297.56, 5.92);
  graph->SetPoint( 5, 307.59, 5.83);
  graph->SetPoint( 6, 316.83, 5.76);
  graph->SetPoint( 7, 327.60, 5.67);
  graph->SetPoint( 8, 337.67, 5.63);
  graph->SetPoint( 9, 347.77, 5.63);
  graph->SetPoint(10, 357.78, 5.53);
  graph->SetPoint(11, 367.77, 5.40);
  graph->SetPoint(12, 377.74, 5.26);
  graph->SetPoint(13, 387.69, 5.10);
  graph->SetPoint(14, 397.64, 4.96);
  graph->SetPoint(15, 407.55, 4.78);
  graph->SetPoint(16, 417.44, 4.59);
  graph->SetPoint(17, 427.34, 4.42);
  graph->SetPoint(18, 437.27, 4.29);
  graph->SetPoint(19, 447.19, 4.16);
  graph->SetPoint(20, 457.00, 3.95);
  graph->SetPoint(21, 466.83, 3.78);
  graph->SetPoint(22, 476.61, 3.60);
  graph->SetPoint(23, 486.41, 3.44);
  graph->SetPoint(24, 496.26, 3.32);
  graph->SetPoint(25, 505.97, 3.15);
  graph->SetPoint(26, 515.66, 2.98);
  graph->SetPoint(27, 525.44, 2.86);
  graph->SetPoint(28, 535.20, 2.74);
  graph->SetPoint(29, 544.87, 2.61);
  graph->SetPoint(30, 554.58, 2.49);
  graph->SetPoint(31, 564.44, 2.43);
  graph->SetPoint(32, 574.31, 2.37);
  graph->SetPoint(33, 584.20, 2.31);
  graph->SetPoint(34, 594.10, 2.26);
  graph->SetPoint(35, 603.69, 2.15);
  graph->SetPoint(36, 613.23, 2.03);
  graph->SetPoint(37, 622.91, 1.95);
  graph->SetPoint(38, 632.66, 1.89);
  graph->SetPoint(39, 642.40, 1.82);
  graph->SetPoint(40, 652.12, 1.75);
  graph->SetPoint(41, 661.70, 1.68);
  graph->SetPoint(42, 671.27, 1.60);
  graph->SetPoint(43, 680.83, 1.51);
  return graph;
}

/*
Obs


*/
