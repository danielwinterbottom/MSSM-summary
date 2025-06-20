import os
import yaml
import pandas as pd
import re
from scipy.interpolate import NearestNDInterpolator, LinearNDInterpolator, RBFInterpolator
import ROOT
import argparse
import pickle
from contour_tools import *
import random
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark', type=str, default='mh125EFT', help='Benchmark scenario')
parser.add_argument('--overwrite', action='store_true', help='Overwrite existing interpolator data')
parser.add_argument('--interp_method', type=str, default='nearest', choices=['nearest','linear','RBF'], help='Interpolation method to use')
parser.add_argument('--test_rm_width', action='store_true', help='Removes half of the width points from the dataset for testing purposes')
args = parser.parse_args()

def parse_filename(filename):
    # Extract mass and width from both 'a_' and 'h_' parts
    pattern = r'a_m(?P<mass_a>\d+)_w(?P<wa1>\d+)p(?P<wa2>\d+).*h_m(?P<mass_h>\d+)_w(?P<wh1>\d+)p(?P<wh2>\d+)'
    match = re.search(pattern, filename)
    if not match:
        return None, None

    mass_a = int(match.group("mass_a"))
    mass_h = int(match.group("mass_h"))

    width_a = float(f"{match.group('wa1')}.{match.group('wa2')}")
    width_h = float(f"{match.group('wh1')}.{match.group('wh2')}")

    if mass_a != mass_h or width_a != width_h:
        return None, None  # Require exact match

    return mass_a, width_a

def extract_variable(variables, name):
    """Find a variable by name and return the first value (or unique if all same)"""
    for var in variables:
        if var["header"]["name"] == name:
            values = [v["value"] for v in var["values"]]
            unique = list(set(values))
            if len(unique) == 1:
                return unique[0]
            return values[0]  # fallback: return first if multiple values
    return None

def load_yaml_files_to_dataframe(directory):
    data = []

    for file in os.listdir(directory):
        if not file.endswith(".yaml"):
            continue

        mass, width = parse_filename(file)
        if mass is None:
            continue

        with open(os.path.join(directory, file), "r") as f:
            print(f"Loading file: {file} (mass={mass}, width={width})")
            content = yaml.safe_load(f)

        indep_vars = content.get("independent_variables", [])
        dep_vars = content.get("dependent_variables", [])

        # Extract all values lists for each variable
        def get_all_values(variables, name):
            for var in variables:
                if var["header"]["name"] == name:
                    return [v["value"] for v in var["values"]]
            return []

        g_A_values = get_all_values(indep_vars, "$g_{A t \\bar t}$")
        g_H_values = get_all_values(indep_vars, "$g_{H t \\bar t}$")
        nll_values = get_all_values(dep_vars, "-2dNLL")

        # check nll_values for negative values
        if any(nll < 0 for nll in nll_values):
            # if negatives are found then shift all the values by the minimum value
            print(f"Warning: Negative -2dNLL values found in file {file}. Shifting all values to be non-negative.")
            min_nll = min(nll_values)
            nll_values = [nll - min_nll for nll in nll_values]

        # Sanity check lengths
        n_entries = min(len(g_A_values), len(g_H_values), len(nll_values))

        for i in range(n_entries):
            row = {
                "mass": mass,
                "rel_width": width / 100,
                "g_A": g_A_values[i],
                "g_H": g_H_values[i],
                "-2dNLL": nll_values[i],
            }
            data.append(row)

    unique_masses = list(set(row["mass"] for row in data))
    # sort unique masses, smallest first
    unique_masses.sort()
    print(f"Unique masses found: {unique_masses}")

    if args.test_rm_width:
        # Remove half of the width points for testing
        unique_widths = list(set(row["rel_width"] for row in data))
        if len(unique_widths) > 1:
            # remove odd indexes from the list of unique widths
            print(f"Unique widths before removal: {unique_widths}")
            half_widths = [unique_widths[i] for i in range(len(unique_widths)) if i % 2 == 1] # remove middle width (usually there are only 3 points provided)
            data = [row for row in data if row["rel_width"] not in half_widths]
            print(f"Removed half of the width points for testing: {half_widths}")

    return pd.DataFrame(data), unique_masses

def build_interpolator(df, masses):
    interpolator_map = {}
    if args.interp_method == 'nearest':
        name = 'interpolator_nearest'
    elif args.interp_method == 'linear':
        name = 'interpolator_linear'
    elif args.interp_method == 'RBF':
        name = 'interpolator_RBF'
    # build a seperate interpolator for each mass point
    for m in masses:
        print(f"Building interpolator for mass {m} GeV...")
        df_m = df[df["mass"] == m]
        x = df_m[["rel_width", "g_A", "g_H"]]
        y = df_m["-2dNLL"]
        if df_m.empty:
            print(f"No data for mass {m}, skipping...")
            continue

        if args.interp_method == 'nearest': interpolator = NearestNDInterpolator(x,y)
        elif args.interp_method == 'linear': interpolator = LinearNDInterpolator(x,y)
        elif args.interp_method == 'RBF': interpolator = RBFInterpolator(x, y)  # smooth=0.0 for exact interpolation
    
        interpolator_map[m] = interpolator
    print(f"Built interpolators for {len(interpolator_map)} mass points.")

    name+='_alt'
    if args.test_rm_width:
        name += "_test_rm_width"

    # store these as pkl files for later use
    interpolator_file = f"{name}.pkl"
    print(f"Saving interpolator to {interpolator_file}...")
    with open(interpolator_file, "wb") as f:
        pickle.dump(interpolator_map, f)
    return interpolator_map

def interpolate_nll(df, interpolator, mass, rel_width, g_A, g_H):
    cl_0p95 = ROOT.Math.chisquared_quantile_c(1 - 0.95, 2)
    nearest_interpolator = NearestNDInterpolator(df[["rel_width", "g_A", "g_H"]], df["-2dNLL"]) # used as fall back incase linear interpolator fails

    # if the width is smaller than the smallest width in the dataset then we clamp it to the smallest width - i.e we assume we are beyond the NWA limit
    min_width = df[df["mass"] == mass]["rel_width"].min()
    clamped_width = max(rel_width, min_width)
    point = [clamped_width, g_A, g_H]

    max_width = df[df["mass"] == mass]["rel_width"].max()
    min_g_A = df[df["mass"] == mass]["g_A"].min()
    min_g_H = df[df["mass"] == mass]["g_H"].min()
    max_g_A = df[df["mass"] == mass]["g_A"].max()
    max_g_H = df[df["mass"] == mass]["g_H"].max()
    
    # print all max and min values for g_A, g_H, and width
    #print(f"Minimum values - g_A: {min_g_A}, g_H: {min_g_H}, rel_width: {min_width}")
    #print(f"Maximum values - g_A: {max_g_A}, g_H: {max_g_H}, rel_width: {max_width}")
        
    # if width is beyond the maximum then we don't exclude the point    
    if clamped_width > max_width:
        excluded = False
        result = -9999
    else:
        result = interpolator[mass](point)[0]
        excluded = result>cl_0p95

        # define some additional default behavior depending on the values of g_A and g_H to prevent out of distribution evaluations
        point_orig = point.copy()  # keep original point for debugging
        # if g_A and g_H are less than the minimum values then we don't exclude
        if g_A < min_g_A and g_H < min_g_H:
            excluded = False
            result = -9999.
        # if only one of g_A or g_H is below the minimum then set it to the minimum value and re-evaluate
        elif g_A < min_g_A:
            g_A = min_g_A
            point[2] = g_A
            result = interpolator[mass](point)[0]
            excluded = result > cl_0p95
        elif g_H < min_g_H:
            g_H = min_g_H
            point[3] = g_H
            result = interpolator[mass](point)[0]
            excluded = result > cl_0p95
        # if both are larger than the maximum values then exclude
        elif g_A > max_g_A and g_H > max_g_H:
            excluded = True
            result = 9999
        # if only one is larger than the maximum then set it to the maximum value and re-evaluate
        elif g_A > max_g_A:
            g_A = max_g_A
            point[2] = g_A
            result = interpolator[mass](point)[0]
            excluded = result > cl_0p95
        elif g_H > max_g_H:
            g_H = max_g_H
            point[3] = g_H
            result = interpolator[mass](point)[0]
            excluded = result > cl_0p95

    # if after all this we still get a nan for the result we fall back to nearest neighbor interpolation
    if np.isnan(result):
        print(f"Warning: Interpolator returned NaN for mass {mass}, rel_width {rel_width}, g_A {g_A}, g_H {g_H}. Falling back to nearest neighbor interpolation.")
        # use the nearest neighbor interpolator for this point
        result = nearest_interpolator(point_orig)[0]
        excluded = result > cl_0p95

    return result, excluded

if args.interp_method == 'nearest':
    name = 'interpolator_nearest'
elif args.interp_method == 'linear':
    name = 'interpolator_linear'
elif args.interp_method == 'RBF':
    name = 'interpolator_RBF'

name+='_alt'
if args.test_rm_width:
    name += "_test_rm_width"


# check if interpolator*_data.pkl and interpolator*.pkl exist
if (os.path.exists(f"{name}_data.pkl") and os.path.exists(f"{name}.pkl")) and not args.overwrite:
    print("Loading existing interpolator...")

    with open(f"{name}_data.pkl", "rb") as f:
        df_clean, masses = pickle.load(f)

    with open(f"{name}.pkl", "rb") as f:
        interpolator_map = pickle.load(f)
    
else:
    print("Loading YAML files and building interpolator...")
    df, masses = load_yaml_files_to_dataframe("yaml_files/XTottbarRun2/")
    df_clean = df.dropna()

    #store both df and masses to same pickle file
    with open(f"{name}_data.pkl", "wb") as f:
        pickle.dump((df_clean, masses), f)
    print(f"Loaded {len(df)} entries from YAML files.")
    print(f"Building interpolator...")
    interpolator_map = build_interpolator(df, masses)
    print("Finished building interpolator.")


# get MSSM benchmark file
mssm_bm_file = f"root_files/{args.benchmark}_13.root"
f = ROOT.TFile(mssm_bm_file)

h_g_A = f.Get('rescale_gt_A')
h_g_H = f.Get('rescale_gt_H')
h_width_A = f.Get('width_A')
h_mass_A = f.Get('m_A')
h_rel_width_A = h_width_A.Clone('h_rel_width_A')
h_rel_width_A.Divide(h_mass_A)

# make a histogram which will store values of 1 when the point is excluded or 0 otherwise

tanb_range = (h_mass_A.GetYaxis().GetBinLowEdge(1),5)
N_values=100
# we want to evaluate every tanb value in tanb_range for N_values points
tanb_values = np.linspace(tanb_range[0], tanb_range[1], N_values)

import time

g_excluded_obs = ROOT.TGraph()

for m in masses:
    print(f"Processing mass {m} GeV...")
    # get the interpolator for this mass

    for tanb in tanb_values:
        #print(f"Processing tanb={tanb} for mass {m} GeV...")
        rel_width = h_rel_width_A.Interpolate(m, tanb)
        g_A = abs(h_g_A.Interpolate(m, tanb))
        g_H = abs(h_g_H.Interpolate(m, tanb))
        start_time = time.time()
        est_nll, excluded = interpolate_nll(df_clean, interpolator_map, mass=m, rel_width=rel_width, g_A=g_A, g_H=g_H)
        elapsed_time = time.time() - start_time
        #print(f"mA={m}, tanb={tanb}, g_A={g_A}, g_H={g_H}, rel_width={rel_width}, -2dNLL={est_nll}, Excluded={excluded}, Time taken: {elapsed_time:.6f} seconds")

        # if point is excluded then add it to the graph
        if excluded:
            g_excluded_obs.SetPoint(g_excluded_obs.GetN(), m, tanb)

# save the histograms
name_extra='_alt'

if args.test_rm_width:
    name_extra = '_test_rm_width'

fout = ROOT.TFile(f'{args.benchmark}_XToTTbar_mAtanb_contours_{args.interp_method}{name_extra}.root', 'recreate')
# write the graph to the file
g_excluded_obs.Write("g_obs_excluded")

# get max and min tanb excluded values for each mass point
tanb_excluded_min = {}
tanb_excluded_max = {}
for i in range(g_excluded_obs.GetN()):
    mA = g_excluded_obs.GetX()[i]
    tanb = g_excluded_obs.GetY()[i]
    if mA not in tanb_excluded_min:
        tanb_excluded_min[mA] = tanb
        tanb_excluded_max[mA] = tanb
    else:
        if tanb < tanb_excluded_min[mA]:
            tanb_excluded_min[mA] = tanb
        if tanb > tanb_excluded_max[mA]:
            tanb_excluded_max[mA] = tanb

contour_obs_0 = ROOT.TGraph()
sorted_masses = sorted(tanb_excluded_min.keys())
contour_obs_0.SetPoint(contour_obs_0.GetN(), sorted_masses[0], tanb_excluded_min[sorted_masses[0]])

for mA in sorted_masses:
    tanb_max = tanb_excluded_max[mA]
    contour_obs_0.SetPoint(contour_obs_0.GetN(), mA, tanb_max)
for mA in reversed(sorted_masses):
    tanb_min = tanb_excluded_min[mA]
    contour_obs_0.SetPoint(contour_obs_0.GetN(), mA, tanb_min)

contour_obs_0.Write("contour_obs_0")