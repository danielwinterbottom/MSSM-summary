#!/usr/bin/env python3
import ROOT
import argparse
import os
import ctypes

def get_xy(g, i):
    """
    Robustly get (x,y) from a TGraph at index i across PyROOT versions.
    Prefer GetPointX/GetPointY, fall back to GetPoint with ctypes.
    """
    if hasattr(g, "GetPointX") and hasattr(g, "GetPointY"):
        return float(g.GetPointX(i)), float(g.GetPointY(i))
    x = ctypes.c_double(0.0)
    y = ctypes.c_double(0.0)
    g.GetPoint(i, x, y)
    return x.value, y.value

def get_contours(rootfile, kind="exp"):
    """
    Get contours for 'exp' or 'obs'.
    Prefer contour_{kind}_{0,1,2,...}; fallback to contour_cmb_{kind}.
    Return list of cloned TGraph.
    """
    gs = []
    for i in range(0, 50):
        g = rootfile.Get(f"contour_{kind}_{i}")
        if not g:
            break
        gs.append(g.Clone(f"{g.GetName()}_{kind}_clone"))

    if len(gs) == 0:
        g = rootfile.Get(f"contour_cmb_{kind}")
        if g:
            gs.append(g.Clone(f"contour_cmb_{kind}_clone"))

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
        out.append((label.strip(), path.strip()))
    return out

def label_to_splitline(label):
    """
    Allow multi-line legend labels using '|' as separator.
    Example: "H #rightarrow WW|HIG-20-016" -> "#splitline{H #rightarrow WW}{HIG-20-016}"
    """
    if "|" not in label:
        return label
    a, b = label.split("|", 1)
    return f"#splitline{{{a}}}{{{b}}}"

def set_fill_alpha(obj, color, alpha):
    """
    ROOT version-safe fill alpha.
    """
    if hasattr(obj, "SetFillColorAlpha"):
        obj.SetFillColorAlpha(color, alpha)
        obj.SetFillStyle(1001)
    else:
        # fallback: no true alpha, use hatch
        obj.SetFillColor(color)
        obj.SetFillStyle(3001)

def make_fill_polygon(g, y_bound, name):
    """
    Turn a contour polyline g into a filled polygon by closing it to y=y_bound.
    Assumes g points are ordered along the contour.
    """
    n = g.GetN()
    if n < 2:
        return None

    xs, ys = [], []
    for i in range(n):
        x, y = get_xy(g, i)
        xs.append(x)
        ys.append(y)

    poly = ROOT.TGraph(n + 3)
    poly.SetName(name)

    # follow contour
    for i in range(n):
        poly.SetPoint(i, xs[i], ys[i])

    # close to boundary
    poly.SetPoint(n + 0, xs[-1], y_bound)
    poly.SetPoint(n + 1, xs[0],  y_bound)
    poly.SetPoint(n + 2, xs[0],  ys[0])  # close

    return poly

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanb", type=float, default=0.1, help="tan(beta) for label only")
    ap.add_argument("--out", type=str, default="summary_expected_fill.pdf")
    ap.add_argument("--xmin", type=float, default=125.0)
    ap.add_argument("--xmax", type=float, default=1000.0)
    ap.add_argument("--ymin", type=float, default=-0.5)
    ap.add_argument("--ymax", type=float, default=0.5)
    ap.add_argument("--cmslabel", type=str, default="CMS Preliminary")
    ap.add_argument("--lumi", type=str, default="138 fb^{-1} (13 TeV)")
    ap.add_argument("--fill_alpha", type=float, default=0.20, help="Fill transparency for channels")
    ap.add_argument("--ch", action="append", default=[],
                    help='Channel spec "LABEL:/path/to/file.root". Repeatable.')
    args = ap.parse_args()

    if len(args.ch) == 0:
        raise RuntimeError('No channels provided. Use repeated --ch "LABEL:FILE.root".')

    channels = parse_channel_specs(args.ch)

    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)

    # Color cycle: if you pass HH,WW,ZZ in this order, you get green, magenta, red
    colors = [
        ROOT.kGreen + 2,
        ROOT.kMagenta + 1,
        ROOT.kRed + 1,
        ROOT.kAzure + 1,
        ROOT.kOrange + 7,
        ROOT.kViolet + 7,
        ROOT.kTeal + 3,
    ]

    # Canvas + pads
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

    # Left pad: frame
    padL.cd()
    frame = ROOT.TH2F("frame", ";m_{H} [GeV];sin#alpha",
                      100, args.xmin, args.xmax, 100, args.ymin, args.ymax)
    frame.GetXaxis().SetTitleSize(0.055)
    frame.GetYaxis().SetTitleSize(0.055)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)
    frame.Draw()

    # CMS labels
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextFont(42)

    latex.SetTextSize(0.050)
    latex.SetTextAlign(11)  # left
    latex.DrawLatex(0.14, 0.93, args.cmslabel)

    latex.SetTextSize(0.045)
    latex.SetTextAlign(31)  # right
    latex.DrawLatex(0.98, 0.93, args.lumi)

    legend_handles = []   # (handle, label, opt)
    channel_outlines = [] # store line graphs to draw on top
    fill_polys_keep = []  # keep references alive

    for idx, (label, path) in enumerate(channels):
        if not os.path.exists(path):
            raise RuntimeError(f"File not found: {path}")

        f = ROOT.TFile.Open(path, "READ")
        if not f or f.IsZombie():
            raise RuntimeError(f"Cannot open ROOT file: {path}")

        gs = get_contours(f, kind="exp")
        if len(gs) == 0:
            raise RuntimeError(f"No expected contours found in {path} (searched contour_exp_* and contour_cmb_exp)")

        col = colors[idx % len(colors)]
        leg_label = label_to_splitline(label)

        # Fill polygons for each segment
        fill_polys = []
        for j, g in enumerate(gs):
            n = g.GetN()
            if n <= 1:
                continue

            # Decide upper/lower branch by average y
            ysum = 0.0
            for i in range(n):
                _, y = get_xy(g, i)
                ysum += y
            yavg = ysum / float(n)

            yb = args.ymax if yavg >= 0 else args.ymin
            poly = make_fill_polygon(g, yb, f"fill_{idx}_{j}")
            if poly:
                set_fill_alpha(poly, col, args.fill_alpha)
                poly.SetLineColor(col)
                poly.SetLineWidth(2)
                fill_polys.append(poly)
                fill_polys_keep.append(poly)

            # Outline styling
            g.SetLineColor(col)
            g.SetLineWidth(3)
            g.SetLineStyle(1)
            channel_outlines.append(g)

        # Draw fills first
        for poly in fill_polys:
            poly.Draw("F same")

        # Legend handle: prefer fill
        if len(fill_polys) > 0:
            legend_handles.append((fill_polys[0], leg_label, "f"))
        else:
            legend_handles.append((gs[0], leg_label, "l"))

        f.Close()

    # Draw outlines on top
    for g in channel_outlines:
        g.Draw("L same")

    # Right pad legend panel
    padR.cd()
    leg = ROOT.TLegend(0.08, 0.15, 0.95, 0.88)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.080)

    latexR = ROOT.TLatex()
    latexR.SetNDC(True)
    latexR.SetTextFont(42)
    latexR.SetTextSize(0.080)
    latexR.SetTextAlign(11)
    latexR.DrawLatex(0.10, 0.92, f"tan#beta = {args.tanb:g}")
    latexR.DrawLatex(0.10, 0.84, "Expected exclusion (95% CL)")

    for h, lab, opt in legend_handles:
        leg.AddEntry(h, lab, opt)
    leg.Draw()

    c.SaveAs(args.out)
    print(f"[ok] wrote {args.out}")

if __name__ == "__main__":
    main()