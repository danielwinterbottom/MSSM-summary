#!/usr/bin/env python3
import ROOT
import sys
import os
import math
import argparse
import numpy as np
from ctypes import c_double

try:
    import yaml
except ImportError:
    raise RuntimeError("PyYAML is required. Please install it first, e.g. pip install pyyaml")

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../python")
from common import *

ROOT.gROOT.SetBatch(True)


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)



def expand_template(s, tanb_str, tanb_value):
    if s is None:
        return None
    if not isinstance(s, str):
        return s
    return (
        s.replace("{tanb}", str(tanb_str))
         .replace("{tanb_value}", str(tanb_value))
    )

def safe_open(path):
    f = ROOT.TFile.Open(path)
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open ROOT file: {path}")
    return f


def clone_obj_from_file(file_path, obj_name):
    f = safe_open(file_path)
    obj = f.Get(obj_name)
    if not obj:
        f.Close()
        raise RuntimeError(f"Cannot find object '{obj_name}' in file '{file_path}'")
    out = obj.Clone(f"{obj.GetName()}__clone")
    if hasattr(out, "SetDirectory"):
        out.SetDirectory(0)
    f.Close()
    return out

CUSTOM_COLORS = {}
CUSTOM_COLOR_OBJECTS = {}

def register_color(name, hexstr, alpha=None):
    hexstr = hexstr.lstrip("#")
    r = int(hexstr[0:2], 16) / 255.0
    g = int(hexstr[2:4], 16) / 255.0
    b = int(hexstr[4:6], 16) / 255.0

    idx = ROOT.TColor.GetFreeColorIndex()

    if alpha is None:
        col = ROOT.TColor(idx, r, g, b, name)
    else:
        col = ROOT.TColor(idx, r, g, b, name, float(alpha))

    CUSTOM_COLORS[name] = idx
    CUSTOM_COLOR_OBJECTS[name] = col

def resolve_color(spec):
    if spec is None:
        raise RuntimeError("Color spec is None")

    if isinstance(spec, int):
        return spec

    if isinstance(spec, float):
        return int(spec)

    if not isinstance(spec, str):
        raise RuntimeError(f"Unsupported color spec type: {type(spec)}")

    spec = spec.strip()

    if spec.startswith("#") and len(spec) == 7:
        return ROOT.TColor.GetColor(spec)

    if spec.lstrip("-").isdigit():
        return int(spec)

    if spec.startswith("ROOT."):
        spec = spec.replace("ROOT.", "", 1)

    if spec in CUSTOM_COLORS:
        return CUSTOM_COLORS[spec]

    g = globals()
    if spec in g:
        obj = g[spec]
        if hasattr(obj, "GetNumber"):
            return obj.GetNumber()
        if isinstance(obj, int):
            return obj

    for sign in ["+", "-"]:
        if sign in spec:
            base, offset = spec.split(sign, 1)
            base_val = resolve_color(base)
            off_val = int(offset)
            return base_val + off_val if sign == "+" else base_val - off_val

    if hasattr(ROOT, spec):
        obj = getattr(ROOT, spec)
        if isinstance(obj, int):
            return obj

    raise RuntimeError(f"Unknown color spec: {spec}")

def get_line_handle(line_color, line_width=2, line_style=1):
    g = ROOT.TGraph()
    g.SetLineColor(line_color)
    g.SetLineWidth(line_width)
    g.SetLineStyle(line_style)
    return g


def get_fill_handle(fill_color, line_color):
    g = ROOT.TGraph()
    g.SetFillColor(fill_color)
    g.SetLineColor(line_color)
    return g


def clip_hist_xmax(h, xmax):
    """
    Set bins with x > xmax to 0 (so they won't be filled, and contour won't extend).
    Works for TH2.
    """
    if xmax is None:
        return h

    xmax = float(xmax)
    xax = h.GetXaxis()
    nbx = h.GetNbinsX()
    nby = h.GetNbinsY()

    # find the first bin center > xmax, then zero from there to the end
    # safer: use bin low edge comparison
    for ix in range(1, nbx + 1):
        # low edge of bin
        xlow = xax.GetBinLowEdge(ix)
        xup  = xax.GetBinUpEdge(ix)
        if xlow >= xmax or xup > xmax:
            for jx in range(ix, nbx + 1):
                for iy in range(1, nby + 1):
                    h.SetBinContent(jx, iy, 0.0)
            break

    return h

def DrawObsHist(hist, fill_color, line_color):
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("")
    hist.GetYaxis().SetTitle("")
    hist.SetFillColor(fill_color)
    hist.Draw("BOXsame")
    hist.SetLineColor(line_color)
    hist.SetContour(1, np.array([0.5], dtype="float64"))
    hist.Draw("CONT3same")
    return get_fill_handle(fill_color, line_color)


def DrawExpHist(hist, line_color, line_width=2):
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("")
    hist.GetYaxis().SetTitle("")
    hist.SetLineColor(line_color)
    hist.SetContour(1, np.array([0.5], dtype="float64"))
    hist.SetLineWidth(line_width)
    hist.Draw("CONT3same")


def PlotGraphObs(g, line_color, fill_color):
    g.SetLineColor(line_color)
    g.SetLineStyle(1)
    g.SetLineWidth(1)
    g.SetMarkerColor(line_color)
    g.SetFillColor(fill_color)
    g.SetFillStyle(1001)
    g.Draw("Fsame")
    g.Draw("Lsame")


def PlotGraphExp(g, line_color):
    g.SetLineColor(line_color)
    g.SetLineWidth(2)
    g.SetFillStyle(0)
    g.SetLineStyle(1)
    g.Draw("Csame")


def build_h125_band(cfg):
    # defaults from your original script
    obs_mu = cfg.get("obs_mu", 1.014)
    obs_err_down = cfg.get("obs_err_down", 0.053)
    exp_mu = cfg.get("exp_mu", 1.0)
    exp_err_down = cfg.get("exp_err_down", 0.053)

    low_lim_obs = obs_mu - 2.0 * obs_err_down
    low_lim_exp = exp_mu - 2.0 * exp_err_down

    # protect against tiny numerical issues
    low_lim_obs = max(0.0, min(1.0, low_lim_obs))
    low_lim_exp = max(0.0, min(1.0, low_lim_exp))

    sina_lim_obs = np.sin(math.acos(low_lim_obs**0.5))
    sina_lim_exp = np.sin(math.acos(low_lim_exp**0.5))

    g_obs_up = ROOT.TGraph()
    g_obs_up.SetPoint(0, 0.0, 1.0)
    g_obs_up.SetPoint(1, 0.0, sina_lim_obs)
    g_obs_up.SetPoint(2, 100000.0, sina_lim_obs)
    g_obs_up.SetPoint(3, 100000.0, 1.0)
    g_obs_up.SetPoint(4, 0.0, 1.0)

    g_obs_down = ROOT.TGraph()
    g_obs_down.SetPoint(0, 0.0, -1.0)
    g_obs_down.SetPoint(1, 0.0, -sina_lim_obs)
    g_obs_down.SetPoint(2, 100000.0, -sina_lim_obs)
    g_obs_down.SetPoint(3, 100000.0, -1.0)
    g_obs_down.SetPoint(4, 0.0, -1.0)

    g_exp_up = ROOT.TGraph()
    g_exp_up.SetPoint(0, 0.0, sina_lim_exp)
    g_exp_up.SetPoint(1, 100000.0, sina_lim_exp)

    g_exp_down = ROOT.TGraph()
    g_exp_down.SetPoint(0, 0.0, -sina_lim_exp)
    g_exp_down.SetPoint(1, 100000.0, -sina_lim_exp)

    return g_obs_up, g_obs_down, g_exp_up, g_exp_down


def DrawContourLabel(c, label_text, sina_limit):
    x_min, x_max = 125, 1000
    y_min, y_max = 0, sina_limit
    points_in_range = []

    for i in range(c.GetN()):
        x, y = c_double(), c_double()
        c.GetPoint(i, x, y)
        xv = float(x.value)
        yv = float(y.value)
        if x_min <= xv <= x_max and y_min <= yv <= y_max:
            points_in_range.append((xv, yv))

    points_in_range.sort(key=lambda p: p[0])

    if not points_in_range:
        return None

    index = len(points_in_range) - 1
    x, y = points_in_range[index]

    label = ROOT.TLatex(x - 10, y - 0.045, label_text)

    if len(points_in_range) > 10 and index >= 10:
        x_prev, y_prev = points_in_range[index - 10]
        angle = math.degrees(math.atan2(y - y_prev, x - x_prev)) * 1500
        label.SetTextAngle(angle)

    label.SetTextSize(0.03)
    label.SetTextAlign(30)
    label.SetTextColor(ROOT.kBlack)
    return label


def draw_width_contours(cfg, tanb_str, tanb_value, sina_limit, keepalive, legend_entries):
    file_path = expand_template(cfg["file"], tanb_str, tanb_value)
    pattern = expand_template(cfg["pattern"], tanb_str, tanb_value)
    max_count = cfg.get("max_count", 4)

    color = resolve_color(cfg.get("color", "kBlack"))
    width = cfg.get("width", 2)
    style = cfg.get("style", 5)
    label_text = cfg.get("label", None)
    legend_text = cfg.get("legend", None)

    f = safe_open(file_path)
    drawn_any = False
    for i in range(max_count):
        name = pattern.format(i=i)
        c = f.Get(name)
        if not c:
            continue
        cg = c.Clone(f"{name}__clone")
        keepalive.append(cg)

        cg.SetLineColor(color)
        cg.SetLineWidth(width)
        cg.SetLineStyle(style)
        cg.Draw("Lsame")
        drawn_any = True

        if label_text:
            tex = DrawContourLabel(cg, label_text, sina_limit)
            if tex:
                tex.Draw()
                keepalive.append(tex)

    f.Close()

    if drawn_any and legend_text:
        legend_entries.append(("line", get_line_handle(color, width, style), legend_text))


def draw_tgraph_objects(cfg, tanb_str, tanb_value, keepalive, legend_entries):
    file_path = expand_template(cfg["file"], tanb_str, tanb_value)
    objects = cfg.get("objects", [])
    if not objects:
        return

    color = resolve_color(cfg.get("color", "kBlack"))
    width = cfg.get("width", 2)
    style = cfg.get("style", 1)
    draw_opt = cfg.get("draw", "Lsame")
    legend_text = cfg.get("legend", None)

    f = safe_open(file_path)
    drawn_any = False
    for obj_name in objects:
        g = f.Get(obj_name)
        if not g:
            continue
        gc = g.Clone(f"{obj_name}__clone")
        keepalive.append(gc)

        gc.SetLineColor(color)
        gc.SetLineWidth(width)
        gc.SetLineStyle(style)
        gc.Draw(draw_opt)
        drawn_any = True
    f.Close()

    if drawn_any and legend_text:
        legend_entries.append(("line", get_line_handle(color, width, style), legend_text))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="YAML configuration file")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    
    for c in cfg.get("colors", []):
        register_color(c["name"], c["hex"], c.get("alpha", None))
    plot_cfg = cfg.get("plot", {})
    tanb_value = float(plot_cfg.get("tanb", 1.0))
    tanb_str = ("%.1f" % tanb_value).replace(".", "p")

    output_name = expand_template(
        plot_cfg.get("output", "Singlet_limits_tanb{tanb}.pdf"),
        tanb_str, tanb_value
    )
    sina_limit = float(plot_cfg.get("sina_limit", 0.4))
    legend_header = plot_cfg.get("legend_header", f"tan#beta = {tanb_value:.1f}")

    canv = squared_legend_to_right(lower_y=-sina_limit, upper_y=sina_limit)

    keepalive = []
    legend_entries = []

      # draw regions
    for reg in cfg.get("regions", []):
        file_path = expand_template(reg["file"], tanb_str, tanb_value)
        obs_name = reg.get("obs_name", "h_obs_excluded")
        exp_name = reg.get("exp_name", "h_exp_excluded")

        fill_color = resolve_color(reg["fill_color"])
        obs_line_color = resolve_color(reg.get("obs_line_color", reg.get("line_color", "kBlack")))
        exp_line_color = resolve_color(reg.get("exp_line_color", reg.get("line_color", "kBlack")))
        legend_text = reg.get("legend", os.path.basename(file_path))

        h_obs = clone_obj_from_file(file_path, obs_name)
        h_exp = clone_obj_from_file(file_path, exp_name)

        # optional per-channel x cutoff
        xmax_draw = reg.get("xmax_draw", None)
        if xmax_draw is not None:
            clip_hist_xmax(h_obs, xmax_draw)
            clip_hist_xmax(h_exp, xmax_draw)

        keepalive.extend([h_obs, h_exp])

        handle = DrawObsHist(h_obs, fill_color, obs_line_color)
        DrawExpHist(h_exp, exp_line_color)
        keepalive.append(handle)
        legend_entries.append(("fill", handle, legend_text))

    # draw extra lines
    for line_cfg in cfg.get("lines", []):
        ltype = line_cfg.get("type", "")
        if ltype == "width_contour":
            draw_width_contours(line_cfg, tanb_str, tanb_value, sina_limit, keepalive, legend_entries)
        elif ltype == "tgraph_objects":
            draw_tgraph_objects(line_cfg, tanb_str, tanb_value, keepalive, legend_entries)
        else:
            raise RuntimeError(f"Unknown line type: {ltype}")

      # draw bands first (e.g. h125)
    for band in cfg.get("bands", []):
        btype = band.get("type", "")
        if btype == "h125_mu":
            fill_color = resolve_color(band.get("fill_color", "tComb"))
            obs_line_color = resolve_color(band.get("obs_line_color", "kComb"))
            exp_line_color = resolve_color(band.get("exp_line_color", "kCombDark"))
            legend_text = band.get("legend", "#splitline{h(125)}{HIG-21-018}")

            g_obs_up, g_obs_down, g_exp_up, g_exp_down = build_h125_band(band)
            keepalive.extend([g_obs_up, g_obs_down, g_exp_up, g_exp_down])

            PlotGraphObs(g_obs_up, obs_line_color, fill_color)
            PlotGraphObs(g_obs_down, obs_line_color, fill_color)
            PlotGraphExp(g_exp_up, exp_line_color)
            PlotGraphExp(g_exp_down, exp_line_color)

            legend_entries.append(("fill", get_fill_handle(fill_color, obs_line_color), legend_text))

        else:
            raise RuntimeError(f"Unknown band type: {btype}")



    # legend
    leg = ROOT.TLegend(0.67, 0.10, 0.99, 0.94)
    leg.SetHeader(legend_header, "C")
    leg.SetBorderSize(1)
    leg.SetFillStyle(1001)
    leg.SetTextSize(0.035)
    leg.SetFillColor(ROOT.kWhite)

    obs = ROOT.TGraph()
    obs.SetFillColor(ROOT.kGray)

    exp = ROOT.TGraph()
    exp.SetLineColor(1)
    exp.SetFillColor(1)
    exp.SetLineWidth(303)
    exp.SetFillStyle(3004)

    keepalive.extend([obs, exp, leg])

    leg.AddEntry(obs, "#splitline{Observed}{exclusion 95% CL}", "F")
    leg.AddEntry(exp, "#splitline{Expected}{exclusion 95% CL}", "L")

    for kind, handle, text in legend_entries:
        if kind == "fill":
            leg.AddEntry(handle, text, "F")
        elif kind == "line":
            leg.AddEntry(handle, text, "L")

    leg.Draw()
    stamp = ROOT.TLatex()
    stamp.SetNDC(True)
    stamp.SetTextFont(42)
    stamp.SetTextSize(0.038)   # 可微调
    stamp.SetTextAlign(13)     # 右上角对齐 (right-top)

    # legend top is y=0.94, so place it slightly above
    stamp.DrawLatex(0.67, 0.985, "March 2026")
    keepalive.append(stamp)

    canv.Update()
    canv.Print(output_name)

    png_name = output_name
    if png_name.lower().endswith(".pdf"):
        png_name = png_name[:-4] + ".png"
    else:
        png_name = output_name + ".png"

    canv.Print(png_name)

    print(f"[ok] wrote {output_name}")
    print(f"[ok] wrote {png_name}")

if __name__ == "__main__":
    main()