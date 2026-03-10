#!/usr/bin/env python3
import ROOT
import argparse
import os

def get_expected_contours(rootfile):
    """
    Prefer contour_exp_0,1,2,... if present.
    Fall back to contour_cmb_exp.
    Return a list of TGraph (cloned so file can be closed).
    """
    gs = []
    for i in range(0, 50):
        g = rootfile.Get(f"contour_exp_{i}")
        if not g:
            break
        gc = g.Clone(f"{g.GetName()}_clone")
        gs.append(gc)

    if len(gs) == 0:
        g = rootfile.Get("contour_cmb_exp")
        if g:
            gs.append(g.Clone("contour_cmb_exp_clone"))

    return gs

def parse_channel_specs(ch_specs):
    """
    Parse repeated --ch "LABEL:FILE.root"
    """
    out = []
    for s in ch_specs:
        if ":" not in s:
            raise RuntimeError(f"Bad --ch format: {s}. Use LABEL:FILE.root")
        label, path = s.split(":", 1)
        label = label.strip()
        path = path.strip()
        out.append((label, path))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanb", type=float, default=0.1, help="tan(beta) for label only")
    ap.add_argument("--out", type=str, default="summary_expected.pdf", help="Output file (pdf/png)")
    ap.add_argument("--xmin", type=float, default=125.0)
    ap.add_argument("--xmax", type=float, default=1000.0)
    ap.add_argument("--ymin", type=float, default=-0.5)
    ap.add_argument("--ymax", type=float, default=0.5)
    ap.add_argument("--cmslabel", type=str, default="CMS Preliminary", help="Top-left label")
    ap.add_argument("--lumi", type=str, default="138 fb^{-1} (13 TeV)", help="Top-right label")
    ap.add_argument("--ch", action="append", default=[],
                    help='Channel spec "LABEL:/path/to/file.root". Repeatable, e.g. --ch "HH->bbbb:bbbb.root"')
    args = ap.parse_args()

    if len(args.ch) == 0:
        raise RuntimeError('No channels provided. Use repeated --ch "LABEL:FILE.root".')

    channels = parse_channel_specs(args.ch)

    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)

    # Colors to cycle
    colors = [
        ROOT.kGreen + 2,
        ROOT.kMagenta + 1,
        ROOT.kRed + 1,
        ROOT.kAzure + 1,
        ROOT.kOrange + 7,
        ROOT.kViolet + 7,
        ROOT.kTeal + 3,
        ROOT.kSpring + 5,
        ROOT.kPink + 7,
        ROOT.kGray + 2,
    ]

    # Canvas with two pads: left plot, right legend panel
    c = ROOT.TCanvas("c", "c", 1200, 800)

    padL = ROOT.TPad("padL", "padL", 0.0, 0.0, 0.68, 1.0)
    padR = ROOT.TPad("padR", "padR", 0.68, 0.0, 1.0, 1.0)

    padL.SetLeftMargin(0.12)
    padL.SetRightMargin(0.02)
    padL.SetTopMargin(0.08)
    padL.SetBottomMargin(0.12)

    padR.SetLeftMargin(0.05)
    padR.SetRightMargin(0.05)
    padR.SetTopMargin(0.08)
    padR.SetBottomMargin(0.12)
    padR.SetFillStyle(0)

    padL.Draw()
    padR.Draw()

    # Left pad: frame + contours
    padL.cd()
    frame = ROOT.TH2F("frame", ";m_{H} [GeV];sin#alpha",
                      100, args.xmin, args.xmax, 100, args.ymin, args.ymax)
    frame.Draw()

    # CMS labels
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextFont(42)
    latex.SetTextSize(0.045)
    latex.DrawLatex(0.14, 0.93, args.cmslabel)
    latex.SetTextSize(0.040)
    latex.DrawLatex(0.78, 0.93, args.lumi)

    # Keep handles for legend
    legend_handles = []

    for idx, (label, path) in enumerate(channels):
        if not os.path.exists(path):
            raise RuntimeError(f"File not found: {path}")

        f = ROOT.TFile.Open(path, "READ")
        if not f or f.IsZombie():
            raise RuntimeError(f"Cannot open ROOT file: {path}")

        gs = get_expected_contours(f)
        if len(gs) == 0:
            raise RuntimeError(f"No expected contours found in {path} (looked for contour_exp_* or contour_cmb_exp)")

        col = colors[idx % len(colors)]

        # style and draw all segments for this channel
        for j, g in enumerate(gs):
            g.SetLineColor(col)
            g.SetLineWidth(3)
            g.SetLineStyle(1)  # solid
            g.Draw("L same")

        # use the first segment as legend handle
        legend_handles.append((gs[0], label))

        f.Close()

    # Right pad: legend only
    padR.cd()
    padR.SetFrameFillStyle(0)

    leg = ROOT.TLegend(0.05, 0.15, 0.95, 0.85)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.080)

    # Title text
    latexR = ROOT.TLatex()
    latexR.SetNDC(True)
    latexR.SetTextFont(42)
    latexR.SetTextSize(0.080)
    latexR.DrawLatex(0.10, 0.92, f"tan#beta = {args.tanb:g}")

    latexR.SetTextSize(0.080)
    latexR.DrawLatex(0.10, 0.86, "Expected exclusion (95% CL)")

    # Add channel entries
    for h, lab in legend_handles:
        leg.AddEntry(h, lab, "l")

    leg.Draw()

    c.SaveAs(args.out)
    print(f"[ok] wrote {args.out}")

if __name__ == "__main__":
    main()