# MSSM-summary plots
This repository hosts everything that is required to create CMS high mass MSSM Higgs boson summary plots. It includes the following sub-directories: 

- **Run-2-hMSSM**: contains the script to create the hMSSM summary plot.
- **Run-2-Mh125**: contains the script to create the Mh125 summary plot.
- **Run-2-Mh125EFT**: contains the script to create the Mh125EFT summary plots.
- **MSSM-tools**: contains the most up to date version of `mssm_xs_tools` and further tools to extrapolate cross-section times branch fraction limits into the $m_{\mathrm{A}}$-$\tan\beta$ plane, for those processes, for which such a procedure is applicable. 

The root macros in these directories require a basic root and a recent python 3 installation.

## (Re-)creating current exclusion contours

To (re-)create the summary plots with the existing contours go to the corresponding sub-directory indicating the model of interest and execute: 

```shell
python3 update_MSSM_limits_[hMSSM, mh125, mh125EFT].py
```

For the use of the `mssm_xs_tools` have a look to the [README.md](https://github.com/roger-wolf/MSSM-summary/blob/main/MSSM-tools/README.md) file in the MSSM_tools folder.

## Adding new contours

To add new contours do the following: 

- Get the contours from HEPData (or any other source). Usually a simple figure is sufficient. You might want to use the [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/) in that case. The precision you get from the digitization is by far sufficient for a summary plot. 

- Add the obtained numbers (e.g. values for $m_{\mathrm{A}}$ and $\tan\beta$) in a template header (```.h```) file, e.g. as provided [here](https://github.com/roger-wolf/MSSM-summary/blob/main/HIG-XX-YYY.h). Note that the TGraph requires three arguments: the index (```int``` starting from 0), values for x (e.g. $m_{\mathrm{A}}$) and y (e.g. $\tan\beta$) for each point. While doing so note the following points: 

  - Inside the header file two functions are defined to return the corresponding limit contour as TGraphs, with the suffixes ```*_obs``` for the observed and ```*_exp``` for the expected contour, respectively. 
  - For the observed contour, there are two ways to return the TGraph, steered by the argument ```filled``` that has to be given when calling the function. The value ```filled=false``` is used for line contours (*not filled*); the value ```filled=true``` is used for filled contours. 
  - Make sure to close the contour in case of the observed limit with argument ```filled=true``` to prevent plotting artifacts. The best way to do this is to add three points by hand to the end of the TGraph, e.g. in the following way: highest value in $m_{\mathrm{A}}$, a value $x$ below the lowest value in $\tan\beta$; lowest value in $m_{\mathrm{A}}$, $x$; lowest value in $m_{\mathrm{A}}$ and lowest point in $\tan\beta$.   

- Rename the functions and header file accordingly and move the header file to the directory that corresponds to the model the contour has been provided for. 

- Include the header file and lines for the contours to be drawn as shown for previous examples in the ```.C``` macro that is used for plotting. A code snipped from the file [MSSM_limits_hMSSM.C](https://github.com/roger-wolf/MSSM-summary/blob/main/Run-2-hMSSM/MSSM_limits_hMSSM.C) is given below: 

  ```C++
  #include "HIG-21-001.h"
  
  //...
  void MSSM_limits_hMSSM(){
    //...
    TGraph* g4 = Contour(HIG_21_001_exp, HIG_21_001_obs, kBlue+2, kBlue, tBlue->GetNumber(), true); 
    leg0_->AddEntry(g4, "#splitline{A/H/h #rightarrow #tau#tau}{arxiv:2208.02717^{#scale[1.6]{ #club}}}", "F");
    //...
  }
  ```

- Note that you are supposed to add a legend entry together with each new contour, by hand. The name of the header file and the functions to obtain observed and expected contours from are irrelevant, as long as they are properly called within the ```.C``` macro. It makes sense however to keep them intuitive. For CMS I follow the CADI line tags, for ATLAS I follow the CONF note IDs.  
