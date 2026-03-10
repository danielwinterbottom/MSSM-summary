#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re

try:
    import yaml
except ImportError:
    raise RuntimeError("Missing PyYAML. Install with: pip install pyyaml")

def sanitize(name: str) -> str:
    # 文件名安全：把 ->, 空格, 括号等替换掉
    s = name.strip()
    s = s.replace("→", "to").replace("->", "to")
    s = re.sub(r"[^\w\.\-]+", "_", s)  # 非字母数字._- 都变成 _
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "channel"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_yaml", help="Input YAML (HEPData-like)")
    ap.add_argument("-o", "--outdir", default="json_channels", help="Output directory")
    ap.add_argument("--mass-format", default="{:.1f}", help='Mass key format, default "{:.1f}" -> "250.0"')
    ap.add_argument("--write-bands", action="store_true",
                    help="Also write limit_m1/m2/p1/p2 (filled with same value if no bands available).")
    ap.add_argument("--drop-nonpositive", action="store_true",
                    help="Drop points with value <= 0 (recommended if these are supposed to be upper limits).")
    args = ap.parse_args()

    with open(args.input_yaml, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    masses = [float(v["value"]) for v in data["independent_variables"][0]["values"]]
    depvars = data["dependent_variables"]

    os.makedirs(args.outdir, exist_ok=True)

    for dv in depvars:
        ch_name = dv.get("header", {}).get("name", "channel")
        ch_file = os.path.join(args.outdir, sanitize(ch_name) + ".json")

        vals = dv["values"]
        if len(vals) != len(masses):
            raise RuntimeError(f"Length mismatch for channel '{ch_name}': masses={len(masses)} values={len(vals)}")

        out = {}
        kept = 0
        dropped = 0

        for m, ve in zip(masses, vals):
            v = float(ve["value"])
            if args.drop_nonpositive and v <= 0:
                dropped += 1
                continue

            key = args.mass_format.format(m)
            entry = {
                "observed": v,
                "limit": v,
            }
            if args.write_bands:
                entry.update({
                    "limit_m2": v,
                    "limit_m1": v,
                    "limit_p1": v,
                    "limit_p2": v,
                })
            out[key] = entry
            kept += 1

        # sort by numeric mass
        out = dict(sorted(out.items(), key=lambda kv: float(kv[0])))

        with open(ch_file, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=4, sort_keys=False)

        print(f"[ok] {ch_name:20s} -> {ch_file}  (kept={kept}, dropped={dropped})")

if __name__ == "__main__":
    main()