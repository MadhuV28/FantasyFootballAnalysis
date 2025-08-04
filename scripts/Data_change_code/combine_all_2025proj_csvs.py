import os
import glob
import pandas as pd
from functools import reduce

proj_folder = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj"
output_path = os.path.join(proj_folder, "FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED.csv")

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(proj_folder, "*.csv"))

# Read all CSVs, standardize columns
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    # Standardize column names (strip, upper, remove duplicate spaces)
    df.columns = [col.strip().upper().replace("  ", " ") for col in df.columns]
    # Always keep PLAYER column, rename if needed
    if 'PLAYER' not in df.columns:
        for col in df.columns:
            if col.lower() == 'player':
                df.rename(columns={col: 'PLAYER'}, inplace=True)
    # Some files may not have TEAM, add if missing
    if 'TEAM' not in df.columns:
        df['TEAM'] = ""
    # Ensure TEAM is always string
    df['TEAM'] = df['TEAM'].astype(str)
    dfs.append(df)

# Merge all DataFrames on PLAYER and TEAM, resolving duplicate stat columns
def merge_and_resolve(left, right):
    # Find stat columns (not PLAYER or TEAM)
    stat_cols_left = [c for c in left.columns if c not in ['PLAYER', 'TEAM']]
    stat_cols_right = [c for c in right.columns if c not in ['PLAYER', 'TEAM']]
    # For overlapping stat columns, rename in right before merge
    overlap = set(stat_cols_left) & set(stat_cols_right)
    right_renamed = right.rename(columns={col: f"{col}_right" for col in overlap})
    merged = pd.merge(left, right_renamed, on=['PLAYER', 'TEAM'], how='outer')
    # For each overlapping stat, combine into one column (prefer left, then right)
    for col in overlap:
        merged[col] = merged[col].combine_first(merged[f"{col}_right"])
        merged.drop(columns=[f"{col}_right"], inplace=True)
    return merged

combined = reduce(merge_and_resolve, dfs)

# Fill all NaN with 0
combined = combined.fillna(0)

# Save to CSV
combined.to_csv(output_path, index=False)
print(f"Combined CSV saved to: {output_path}")