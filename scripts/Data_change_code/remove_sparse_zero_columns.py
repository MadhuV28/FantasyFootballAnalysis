import os
import pandas as pd
import glob
import numpy as np

combined_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"

for csv_file in glob.glob(os.path.join(combined_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Skipped {csv_file}: {e}")
        continue

    # Only operate on data rows (skip description row if present)
    header = df.columns
    # If the second row is a description row, skip it for analysis
    if isinstance(df.iloc[0, 0], str) and "fantasy" in df.iloc[1, 0].lower():
        data = df.iloc[2:].reset_index(drop=True)
    else:
        data = df

    # Remove columns with >50% empty or zero values
    cols_to_drop = []
    row_count = len(data)
    for col in header:
        col_data = data[col]
        # Count empty or zero (treat as string or numeric)
        empty_or_zero = col_data.isna() | (col_data == 0) | (col_data == "0") | (col_data == "") | (col_data == " ")
        # Try numeric conversion for more robust zero detection
        try:
            numeric_col = pd.to_numeric(col_data, errors='coerce')
            empty_or_zero = empty_or_zero | (numeric_col == 0)
        except Exception:
            pass
        if empty_or_zero.sum() > (row_count / 2):
            cols_to_drop.append(col)

    if cols_to_drop:
        print(f"Dropping columns from {os.path.basename(csv_file)}: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
        df.to_csv(csv_file, index=False)
    else:
        print(f"No columns dropped from {os.path.basename(csv_file)}")