import os
import pandas as pd

QB_METRICS_PATH = "other/qb_metrics"

for fname in os.listdir(QB_METRICS_PATH):
    if fname.endswith(".csv"):
        fpath = os.path.join(QB_METRICS_PATH, fname)
        df = pd.read_csv(fpath)
        # Find the attempts column (case-insensitive, handles possible variations)
        attempts_col = [col for col in df.columns if "attempt" in col.lower()]
        if attempts_col:
            df_filtered = df[df[attempts_col[0]].astype(float) > 100]
            df_filtered.to_csv(fpath, index=False)
            print(f"Filtered {fpath} to QBs with >100 attempts.")
        else:
            print(f"Skipped {fpath} (no attempts column found.)")