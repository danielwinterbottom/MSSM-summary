import os
import yaml
import pandas as pd
import re
from scipy.interpolate import NearestNDInterpolator, LinearNDInterpolator
import ROOT
import argparse
import pickle
from contour_tools import *
from random import random
import matplotlib.pyplot as plt

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark', type=str, default='mh125EFT', help='Benchmark scenario')
parser.add_argument('--overwrite', action='store_true', help='Overwrite existing interpolator data')
parser.add_argument('--interp_method', type=str, default='nearest', choices=['nearest','linear','NN'], help='Interpolation method to use')
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

    return pd.DataFrame(data)

def build_interpolator(df):
    #interpolator = NearestNDInterpolator(
    if args.interp_method == 'nearest':
        name = 'interpolator_nearest'
        interpolator = NearestNDInterpolator(
            df[["mass", "rel_width", "g_A", "g_H"]],
            df["-2dNLL"]
        )
    elif args.interp_method == 'linear':
        name = 'interpolator_linear'
        interpolator = LinearNDInterpolator(
            df[["mass", "rel_width", "g_A", "g_H"]],
            df["-2dNLL"]
        )

    # store these as pkl files for later use
    interpolator_file = f"{name}.pkl"
    with open(interpolator_file, "wb") as f:
        pickle.dump(interpolator, f)
    return interpolator

def train_keras_nn(df, epochs=50, batch_size=32):
    X = df[["mass", "rel_width", "g_A", "g_H"]].values
    y = df["-2dNLL"].values.reshape(-1, 1)

    # Scale features and target
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X_scaled, y_scaled, test_size=0.1, random_state=42
    )

    # Define model
    model = keras.Sequential([
        layers.Input(shape=(4,)),
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")

    # Early stopping
    early_stop = keras.callbacks.EarlyStopping(
        patience=5, restore_best_weights=True, verbose=1
    )

    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
        verbose=1
    )

    # make a plot of the true and predicted values for train and test
    # scale back to the origional scale 
    y_train_pred = model.predict(X_train, verbose=0)
    y_val_pred = model.predict(X_val, verbose=0)
    y_train_true = scaler_y.inverse_transform(y_train)
    y_val_true = scaler_y.inverse_transform(y_val)
    y_train_pred = scaler_y.inverse_transform(y_train_pred)
    y_val_pred = scaler_y.inverse_transform(y_val_pred)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(y_train_true, y_train_pred, alpha=0.01)
    # plot it like a heatmap
    #plt.hexbin(y_train_true, y_train_pred, gridsize=50, cmap='Blues', mincnt=1)
    plt.plot([y_train_true.min(), y_train_true.max()], [y_train_true.min(), y_train_true.max()], 'r--')
    plt.title("Training")
    plt.xlabel("True -2dNLL")
    plt.ylabel("Predicted -2dNLL")
    plt.subplot(1, 2, 2)
    plt.scatter(y_val_true, y_val_pred, alpha=0.01)
    # plot it like a heatmap
    #plt.hexbin(y_val_true, y_val_pred, gridsize=50, cmap='Blues', mincnt=1)
    plt.plot([y_val_true.min(), y_val_true.max()], [y_val_true.min(), y_val_true.max()], 'r--')
    plt.title("Validation")
    plt.xlabel("True -2dNLL")
    plt.ylabel("Predicted -2dNLL")
    plt.tight_layout()
    plt.savefig(f"{name}_training_results.pdf")
    # also make a histogram plot of true-predicted values
    plt.figure(figsize=(8, 6))
    plt.hist(y_train_true - y_train_pred, bins=50, alpha=0.5, label='Train', density=True)
    plt.hist(y_val_true - y_val_pred, bins=50, alpha=0.5, label='Validation', density=True)
    plt.xlabel("(True - Predicted) -2dNLL")
    plt.legend()
    plt.savefig(f"{name}_training_results_histogram.pdf")

    # make plots of loss vs epoch for training and validation
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(f"{name}_training_loss.pdf")

    return model, scaler_x, scaler_y

def interpolate_nll(df, interpolator, mass, rel_width, g_A, g_H):
    min_width = df["rel_width"].min()
    clamped_width = max(rel_width, min_width)
    #if rel_width < min_width:
    #    print(f"Width {rel_width} is below minimum {min_width}; using {clamped_width} instead.")

    point = [mass, clamped_width, g_A, g_H]

    cl_0p95 = ROOT.Math.chisquared_quantile_c(1 - 0.95, 2)
    
    # define some default behavior depending on the values of the parameters
    # if mass is < minimum mass or > maximum mass in dataframe then don't exclude
    # if width is larger than maximum width in dataframe then don't exclude
    min_mass = df["mass"].min()
    max_mass = df["mass"].max()
    max_width = df["rel_width"].max()
        
    if mass < min_mass or mass > max_mass or clamped_width > min_width:
        excluded = False
        result = 0.
    else:
        result = interpolator(point)[0]
        excluded = result>cl_0p95

    # define some additional default behavior depending on the values of g_A and g_H to prevent out of distribution evaluations
    if result is None or True:
        # if g_A and g_H are less than the minimum values then we don't exclude
        min_g_A = df["g_A"].min()
        min_g_H = df["g_H"].min()
        max_g_A = df["g_A"].max()
        max_g_H = df["g_H"].max()
        if g_A < min_g_A and g_H < min_g_H:
            excluded = False
        # if only one of g_A or g_H is below the minimum then set it to the minimum value and re-evaluate
        elif g_A < min_g_A:
            g_A = min_g_A
            point[2] = g_A
            result = interpolator(point)[0]
            excluded = result > cl_0p95
        elif g_H < min_g_H:
            g_H = min_g_H
            point[3] = g_H
            result = interpolator(point)[0]
            excluded = result > cl_0p95
        # if both are larger than the maximum values then don't exclude
        elif g_A > max_g_A and g_H > max_g_H:
            excluded = False
        # if only one is larger than the maximum then set it to the maximum value and re-evaluate
        elif g_A > max_g_A:
            g_A = max_g_A
            point[2] = g_A
            result = interpolator(point)[0]
            excluded = result > cl_0p95
        elif g_H > max_g_H:
            g_H = max_g_H
            point[3] = g_H
            result = interpolator(point)[0]
            excluded = result > cl_0p95
        #else: 
        #    print('Warning: Exclusion determination failed for parameters mass={}, rel_width={}, g_A={}, g_H={}'.format(mass, clamped_width, g_A, g_H))
        #    print('This should not happen if the input data is correct.')
        #    excluded = False # as backup if all else fails we don't exclude the point

    return result, excluded


if args.interp_method == 'nearest':
    name = 'interpolator_nearest'
elif args.interp_method == 'linear':
    name = 'interpolator_linear'
elif args.interp_method == 'NN':
    name = 'interpolator_NN'

# check if interpolator*_data.pkl and interpolator*.pkl exist
if (os.path.exists(f"{name}_data.pkl") and os.path.exists(f"{name}.pkl")) and not args.overwrite:
    print("Loading existing interpolator...")

    df_clean = pd.read_pickle(f"{name}_data.pkl")

    if args.interp_method == 'NN':
        with open(f"{name}_model.pkl", "rb") as f:
            model, scalar_x, scalar_y = pickle.load(f)
        print("Loaded NN model and scalers.")
    else:
        with open(f"{name}.pkl", "rb") as f:
            interpolator = pickle.load(f)
    
else:
    print("Loading YAML files and building interpolator...")
    df = load_yaml_files_to_dataframe("yaml_files/XTottbarRun2/")
    df_clean = df.dropna()
    # print df when -2dNLL values are negative
    if len(df_clean[df_clean["-2dNLL"] < 0]) > 0:
        print("Warning: Negative -2dNLL values found:")
        # sort the -ve values with largest absolute value first
        df_negative = df_clean[df_clean["-2dNLL"] < 0].sort_values(by="-2dNLL", ascending=True)
        print(df_negative)
        # save the negative values to a separate file
        df_negative.to_csv("negative_2dNLL_values.csv", index=False)
    df_clean.to_pickle(f"{name}_data.pkl")
    print(f"Loaded {len(df)} entries from YAML files.")
    print(f"Building interpolator...")
    if args.interp_method == 'NN':
        model, scaler_x, scaler_y = train_keras_nn(df_clean)
        # save with pickle
        with open(f"{name}_model.pkl", "wb") as f:
            pickle.dump((model, scaler_x, scaler_y), f)
    else:
        interpolator = build_interpolator(df)

if args.interp_method == 'NN':
    with open(f"{name}_model.pkl", "rb") as f:
        model, scalar_x, scalar_y = pickle.load(f)
    # define interpolator function for the NN model
    def interpolator(point):
        X = np.array([point])
        X_scaled = scalar_x.transform(X)
        # Use the NN model to predict the -2dNLL value
        y_scaled = model.predict(X_scaled, verbose=0)
        y = scalar_y.inverse_transform(y_scaled)
        return y[0]

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
mA_range = (300,1000)
tanb_range = (h_mass_A.GetYaxis().GetBinLowEdge(1),5)
Nbins=100

h_excluded_exp = ROOT.TH2D('h_exp','',Nbins,mA_range[0],mA_range[1],Nbins,tanb_range[0],tanb_range[1])
h_excluded_obs = ROOT.TH2D('h_obs','',Nbins,mA_range[0],mA_range[1],Nbins,tanb_range[0],tanb_range[1])

count = 0
for y in range(1,h_excluded_exp.GetNbinsY()+1):
    for x in range(1,h_excluded_exp.GetNbinsX()+1):

        tanb = h_excluded_exp.GetYaxis().GetBinCenter(y)
        mA   = h_excluded_exp.GetXaxis().GetBinCenter(x)

        width = h_rel_width_A.Interpolate(mA, tanb)
        rel_width = width/mA
        g_A = abs(h_g_A.Interpolate(mA, tanb)) # we take absolute values as H/A->ttbar search not sensitive to the sign
        g_H = abs(h_g_H.Interpolate(mA, tanb))

        est_nll, excluded = interpolate_nll(df_clean, interpolator, mass=mA, rel_width=rel_width, g_A=g_A, g_H=g_H)
        
        h_excluded_obs.SetBinContent(x, y, int(excluded))
        # no excluded version provided for now so just use observed as place holder
        h_excluded_exp.SetBinContent(x, y, int(excluded))

        # print the info every 1/1000 events randomly
        rand = random()
        if rand < 0.001:
            print(f"mA={mA}, tanb={tanb}, g_A={g_A}, g_H={g_H}, rel_width={rel_width}, -2dNLL={est_nll}, Excluded={excluded}")
        count += 1

# save the histograms
fout = ROOT.TFile(f'{args.benchmark}_XToTTbar_mAtanb_contours_{args.interp_method}_test.root', 'recreate')
h_excluded_exp.Write("h_exp_excluded")
h_excluded_obs.Write("h_obs_excluded")

# get countours from 2D histograms 
contours_obs = contourFromTH2(h_excluded_obs,1.)
contours_exp = contourFromTH2(h_excluded_exp,1.)

# store integer indicating the number of contours on the output file
n_contours = len(contours_obs)
fout.WriteObject(ROOT.TParameter("int")("n_contours", n_contours), 'n_contours')

# sort countours them by the number of points in the graphs (largest first)
contours_obs = sorted(contours_obs, key=lambda x: x.GetN(), reverse=True)
contours_exp = sorted(contours_exp, key=lambda x: x.GetN(), reverse=True)

# now write all contours to the output file
for i, c in enumerate(contours_obs):
    c.Write(f'contour_obs_{i}')
for i, c in enumerate(contours_exp):
    c.Write(f'contour_exp_{i}')
