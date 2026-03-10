# python3 plot_summary_expected.py \
#   --tanb 0.1 \
#   --out summary_expected_tanb0p1.pdf \
#   --ch "H#rightarrow bbbb:singlet_tanb0p1_ggToHTohh_bbbb_mHsina_contours.root" \
#   --ch "H#rightarrow bbbb(boosted):singlet_tanb0p1_ggToHTohh_bbbb_boosted_mHsina_contours.root"\
#   --ch "H#rightarrow bbtt:singlet_tanb0p1_ggToHTohh_bbtt_mHsina_contours.root"\
#   --ch "H#rightarrow bbWW:singlet_tanb0p1_ggToHTohh_bbww_mHsina_contours.root"\
#   --ch "H#rightarrow multilepton:singlet_tanb0p1_ggToHTohh_multilepton_mHsina_contours.root"\
#   --ch "H#rightarrow bb#gamma#gamma:singlet_tanb0p1_ggToHTohh_bbgg_mHsina_contours.root" 


# python3 plot_summary_expected.py \
#   --tanb 0.1 \
#   --out summary_plot_repeat.pdf \
#   --ch "HH:singlet_tanb0p1_ggToHTohh_mHsina_contours.root" \
#   --ch "WW:singlet_tanb0p1_ggToHToWW_mHsina_contours.root"\
#   --ch "ZZ:singlet_tanb0p1_ggToHToZZ_mHsina_contours.root"

# python3 plot_new.py \
#   --tanb 0.1 \
#   --out summary_plot_fill.pdf \
#   --ch "HH:singlet_tanb0p1_ggToHTohh_mHsina_contours.root" \
#   --ch "WW:singlet_tanb0p1_ggToHToWW_mHsina_contours.root" \
#   --ch "ZZ:singlet_tanb0p1_ggToHToZZ_mHsina_contours.root"

# python3 SingletPlot.py --tanb 0.1
python3 SingletPlot_yaml.py --config plot_config.yaml