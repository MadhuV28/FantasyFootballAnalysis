import os
import pandas as pd
import glob

combined_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"

for csv_file in glob.glob(os.path.join(combined_dir, "*.csv")):
    df = pd.read_csv(csv_file)
    # Detect and preserve description row if present
    has_desc = False
    if len(df) > 1 and (
        "fantasy" in str(df.iloc[1, 0]).lower()
        or "ranking" in str(df.iloc[1, 0]).lower()
        or "player name" in str(df.iloc[1, 0]).lower()
    ):
        header = df.iloc[[0]]
        desc = df.iloc[[1]]
        data = df.iloc[2:].copy()
        has_desc = True
    else:
        header = None
        desc = None
        data = df.copy()
    # Find Fantasy Points column (case-insensitive)
    fp_col = None
    for col in data.columns:
        if col.strip().lower() == "fantasy points":
            fp_col = col
            break
    if fp_col:
        # Sort by Fantasy Points (descending, numeric)
        data[fp_col] = pd.to_numeric(data[fp_col], errors='coerce')
        data = data.sort_values(by=fp_col, ascending=False)
    # Reassemble and write
    if has_desc:
        out_df = pd.concat([header, desc, data], ignore_index=True)
    else:
        out_df = data
    out_df.to_csv(csv_file, index=False)
    print(f"Sorted {os.path.basename(csv_file)} by Fantasy Points")