import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"
out_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb_with_snaps"
os.makedirs(out_dir, exist_ok=True)

for file in glob.glob(os.path.join(rb_dir, "*.csv")):
    df = pd.read_csv(file)
    # Try to find the correct columns by name (case-insensitive)
    rush_col = next((c for c in df.columns if c.strip().lower() == "rushing attempts (advanced)"), None)
    targ_col = next((c for c in df.columns if c.strip().lower() in ["targets (advanced)", "targets"]), None)
    if rush_col and targ_col:
        df["relevent_snaps_played"] = pd.to_numeric(df[rush_col], errors="coerce").fillna(0) + pd.to_numeric(df[targ_col], errors="coerce").fillna(0)
    else:
        df["relevent_snaps_played"] = ""
    out_path = os.path.join(out_dir, os.path.basename(file))
    df.to_csv(out_path, index=False)
    print(f"Processed {file} -> {out_path}")