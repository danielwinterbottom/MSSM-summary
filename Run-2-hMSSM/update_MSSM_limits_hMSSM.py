#!/usr/bin/python3
from sys import argv
from os import system 

if len(argv)>1: 
    if argv[1]=="-c" or argv[1]=="--clean":
        system("rm *~ *.pcm *.d *.so *.pdf *.png")
else:
    system("root -l -b -q -e \".x MSSM_limits_hMSSM.C+\"")
    system("pdftoppm MSSM_limits_hMSSM.pdf MSSM_limits_hMSSM -png -cropbox")
    system("mv MSSM_limits_hMSSM-1.png MSSM_limits_hMSSM.png")
