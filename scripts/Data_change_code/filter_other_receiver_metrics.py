import os
import pandas as pd

def filter_metrics(folder, routes_col_name="routes_run", min_routes=30):
    for fname in os.listdir(folder):
        if fname.endswith(".csv"):
            fpath = os.path.join(folder, fname)
            df = pd.read_csv(fpath)
            # Find the routes column (case-insensitive, handles possible variations)
            routes_cols = [col for col in df.columns if "route" in col.lower()]
            if routes_cols:
                df_filtered = df[df[routes_cols[0]].astype(float) >= min_routes]
                df_filtered.to_csv(fpath, index=False)
                print(f"Filtered {fpath} to receivers with ≥{min_routes} routes.")
            else:
                print(f"Skipped {fpath} (no routes column found.)")

filter_metrics("other/yprr_metrics")
filter_metrics("other/routes_metrics")