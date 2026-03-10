#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

def load_input(path: str):
    """
    Load either YAML or JSON.
    - If PyYAML is available and file looks like YAML, use yaml.safe_load.
    - Otherwise try json.load.
    """
    ext = os.path.splitext(path)[1].lower()
    is_yaml = ext in [".yml", ".yaml"]

    if is_yaml:
        try:
            import yaml  # type: ignore
        except ImportError:
            raise RuntimeError(
                "Input looks like YAML but PyYAML is not installed. "
                "Install with: pip install pyyaml"
            )
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # JSON
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def pick_depvar(dependent_variables, predicate):
    """Return the first dependent_variable whose header name matches predicate."""
    for dv in dependent_variables:
        name = (dv.get("header", {}) or {}).get("name", "") or ""
        if predicate(name):
            return dv
    return None

def find_expected_68(dvs):
    # common patterns: "Expected limit, 68%", "Expected limit 68%", "Expected 68%"
    return pick_depvar(dvs, lambda n: ("Expected" in n) and ("68" in n))

def find_expected_95(dvs):
    return pick_depvar(dvs, lambda n: ("Expected" in n) and ("95" in n))

def find_observed(dvs):
    # common patterns: "Observed limit", "Observed", "Observed 95% CL"
    return pick_depvar(dvs, lambda n: ("Observed" in n))

def get_err_asym(value_entry, label_hint=None):
    """
    Extract asym errors from a value entry:
      value_entry = {"value": ..., "errors":[{"label":"68%","asymerror":{"plus":...,"minus":...}}]}
    Returns (plus, minus) floats or (None, None).
    """
    errs = value_entry.get("errors", []) or []
    if not errs:
        return None, None

    # try to pick by label if provided
    if label_hint is not None:
        for e in errs:
            if str(e.get("label", "")) == str(label_hint):
                ae = e.get("asymerror", {}) or {}
                return ae.get("plus", None), ae.get("minus", None)

    # fallback: first error
    ae = (errs[0].get("asymerror", {}) or {})
    return ae.get("plus", None), ae.get("minus", None)

def lower_from_minus(median, minus):
    # some files store minus as negative (e.g. -0.3), some store as +0.3
    return median + minus if minus is not None and minus < 0 else median - minus

def upper_from_plus(median, plus):
    # some files store plus as positive; if negative, treat as symmetric sign mistake
    return median + plus if plus is not None and plus > 0 else median - plus

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input HEPData-style YAML/JSON")
    ap.add_argument("output", help="Output JSON in flat dict format")
    ap.add_argument("--mass-format", default="{:.1f}",
                    help='Mass key format, default "{:.1f}" -> "300.0"')
    ap.add_argument("--fill-observed-with-expected", action="store_true",
                    help="If no observed dependent variable is found, fill observed=expected median (recommended for compatibility).")
    args = ap.parse_args()

    data = load_input(args.input)

    indep = data["independent_variables"][0]["values"]
    masses = [float(v["value"]) for v in indep]

    dvs = data["dependent_variables"]

    dv68 = find_expected_68(dvs)
    dv95 = find_expected_95(dvs)
    dvobs = find_observed(dvs)

    if dv68 is None:
        raise RuntimeError("Cannot find dependent_variable for Expected 68%. Header name must contain 'Expected' and '68'.")
    if dv95 is None:
        raise RuntimeError("Cannot find dependent_variable for Expected 95%. Header name must contain 'Expected' and '95'.")

    v68 = dv68["values"]
    v95 = dv95["values"]

    if len(v68) != len(masses) or len(v95) != len(masses):
        raise RuntimeError(f"Length mismatch: masses={len(masses)}, exp68={len(v68)}, exp95={len(v95)}")

    vobs = None
    if dvobs is not None:
        vobs = dvobs.get("values", None)
        if vobs is not None and len(vobs) != len(masses):
            raise RuntimeError(f"Length mismatch: masses={len(masses)}, observed={len(vobs)}")

    out = {}

    if dvobs is None and not args.fill_observed_with_expected:
        print("[warning] No observed dependent_variable found. "
              "Output will still include 'observed' but set to null. "
              "If you need compatibility with read_json_to_graphs_NWA, rerun with --fill-observed-with-expected.",
              file=sys.stderr)

    for i, m in enumerate(masses):
        median = float(v68[i]["value"])
        p1, m1 = get_err_asym(v68[i], label_hint="68%")
        p2, m2 = get_err_asym(v95[i], label_hint="95%")

        if p1 is None or m1 is None:
            # fallback: try without label
            p1, m1 = get_err_asym(v68[i], label_hint=None)
        if p2 is None or m2 is None:
            p2, m2 = get_err_asym(v95[i], label_hint=None)

        if p1 is None or m1 is None or p2 is None or m2 is None:
            raise RuntimeError(f"Cannot parse asym errors at mass index {i}, m={m}")

        limit_m1 = float(lower_from_minus(median, float(m1)))
        limit_p1 = float(upper_from_plus(median, float(p1)))
        limit_m2 = float(lower_from_minus(median, float(m2)))
        limit_p2 = float(upper_from_plus(median, float(p2)))

        if vobs is not None:
            obs_val = float(vobs[i]["value"])
        else:
            if args.fill_observed_with_expected:
                obs_val = float(median)
            else:
                obs_val = None

        key = args.mass_format.format(m)
        out[key] = {
            "limit_m2": limit_m2,
            "limit_m1": limit_m1,
            "limit_p1": limit_p1,
            "limit_p2": limit_p2,
            "observed": obs_val,
            "limit": median,
        }

    # sort by numeric mass key
    out_sorted = dict(sorted(out.items(), key=lambda kv: float(kv[0])))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out_sorted, f, indent=4, sort_keys=False)

    print(f"Wrote {len(out_sorted)} mass points to {args.output}")

if __name__ == "__main__":
    main()