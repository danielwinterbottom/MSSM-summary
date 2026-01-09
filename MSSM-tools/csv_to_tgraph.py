#!/usr/bin/env python3
"""
csv_to_tgraph.py

Convert a CSV file into a ROOT TGraph and save it in a ROOT file.

Examples:
  # Basic (first two columns are x,y; auto-detect header)
  python csv_to_tgraph.py data.csv out.root

  # Use specific columns (0-based indices), semicolon delimiter
  python csv_to_tgraph.py data.csv out.root --xcol 1 --ycol 3 --delim ';'

  # Treat first row as header explicitly
  python csv_to_tgraph.py data.csv out.root --has-header

  # Name/title of the graph and object key in ROOT file
  python csv_to_tgraph.py data.csv out.root --name g --title "My Graph"
"""

import argparse
import csv
import sys
from array import array

def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False

def read_csv_points(
    path: str,
    xcol: int,
    ycol: int,
    delim: str,
    skip_rows: int,
    has_header = None,
    comment =None,
):
    xs, ys = [], []

    with open(path, "r", newline="") as f:
        reader = csv.reader(f, delimiter=delim)

        # Skip explicit leading rows
        for _ in range(skip_rows):
            try:
                next(reader)
            except StopIteration:
                return xs, ys

        first_row = None
        for row in reader:
            if not row:
                continue
            if comment and row[0].lstrip().startswith(comment):
                continue
            first_row = row
            break

        if first_row is None:
            return xs, ys

        # Decide header behavior
        if has_header is None:
            # Auto-detect: if x/y entries in first row are not floats, assume header
            auto_header = not (len(first_row) > max(xcol, ycol) and
                               is_float(first_row[xcol].strip()) and
                               is_float(first_row[ycol].strip()))
        else:
            auto_header = has_header

        # If not header, process first_row as data
        if not auto_header:
            row = first_row
            if len(row) <= max(xcol, ycol):
                raise ValueError(f"Row has too few columns: {row}")
            xs.append(float(row[xcol].strip()))
            ys.append(float(row[ycol].strip()))

        # Process remaining rows
        for row in reader:
            if not row:
                continue
            if comment and row[0].lstrip().startswith(comment):
                continue
            if len(row) <= max(xcol, ycol):
                continue  # silently skip short/bad rows
            sx, sy = row[xcol].strip(), row[ycol].strip()
            if not (is_float(sx) and is_float(sy)):
                continue  # skip non-numeric rows
            xs.append(float(sx))
            ys.append(float(sy))

    return xs, ys

def main():
    ap = argparse.ArgumentParser(description="Convert CSV to ROOT TGraph")
    ap.add_argument("--csv", help="Input CSV file")
    ap.add_argument("--root", help="Output ROOT file (e.g. out.root)")
    ap.add_argument("--xcol", type=int, default=0, help="0-based index of x column (default: 0)")
    ap.add_argument("--ycol", type=int, default=1, help="0-based index of y column (default: 1)")
    ap.add_argument("--delim", default=",", help="CSV delimiter (default: ',')")
    ap.add_argument("--skip-rows", type=int, default=0, help="Skip N initial rows before reading (default: 0)")

    hdr = ap.add_mutually_exclusive_group()
    hdr.add_argument("--has-header", action="store_true", help="Treat first non-skipped row as header")
    hdr.add_argument("--no-header", action="store_true", help="Treat first non-skipped row as data")

    ap.add_argument("--comment", default=None,
                    help="Comment prefix for lines to ignore (e.g. '#'). Only checks first field.")
    ap.add_argument("--name", default="g", help="ROOT object name/key (default: g)")
    ap.add_argument("--title", default="", help="Graph title (default: empty)")
    ap.add_argument("--x-title", default="", help="X axis title")
    ap.add_argument("--y-title", default="", help="Y axis title")
    ap.add_argument("--sort-x", action="store_true", help="Sort points by x before writing")

    args = ap.parse_args()

    has_header = None
    if args.has_header:
        has_header = True
    if args.no_header:
        has_header = False

    xs, ys = read_csv_points(
        args.csv, args.xcol, args.ycol, args.delim, args.skip_rows, has_header, args.comment
    )

    if len(xs) == 0:
        print("No valid (x,y) points found in CSV.", file=sys.stderr)
        sys.exit(2)

    if args.sort_x:
        pairs = sorted(zip(xs, ys), key=lambda p: p[0])
        xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]

    # Import ROOT only after we know we have data (and for nicer errors)
    try:
        import ROOT
    except ImportError as e:
        print("ERROR: Could not import ROOT (PyROOT). Make sure ROOT is installed and configured.", file=sys.stderr)
        raise

    ax = array("d", xs)
    ay = array("d", ys)

    g = ROOT.TGraph(len(ax), ax, ay)
    g.SetName(args.name)
    g.SetTitle(args.title)

    if args.x_title:
        g.GetXaxis().SetTitle(args.x_title)
    if args.y_title:
        g.GetYaxis().SetTitle(args.y_title)

    fout = ROOT.TFile(args.root, "RECREATE")
    if not fout or fout.IsZombie():
        print(f"ERROR: Could not create ROOT file: {args.root}", file=sys.stderr)
        sys.exit(3)

    g.Write()  # writes with g.GetName() as key
    fout.Close()

    print(f"Wrote TGraph '{args.name}' with {len(xs)} points to {args.root}")

if __name__ == "__main__":
    main()


