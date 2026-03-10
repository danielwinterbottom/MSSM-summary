# for br in bbbb bbbb_boosted bbgg bbtt bbww bbzz multilepton; do
#   echo ">>> Running: br=${br}"
#   python3 Get_mHsina_regions_HHVV.py --decay hh --br "${br}" --tanb 0.1
# done

# python3 Get_mHsina_regions.py --decay hh --tanb 0.1
# python3 Get_mHsina_regions.py --decay WW  --proc gg+vbf --tanb 0.1 &
python3 Get_mHsina_regions.py --decay ZZ --tanb 4 &
python3 Get_mHsina_regions.py --decay hh --tanb 4 &
python3 Get_mHsina_regions.py --decay WW  --proc gg+vbf --tanb 4 &

