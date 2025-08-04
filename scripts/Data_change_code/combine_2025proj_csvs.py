import os
import pandas as pd
import glob

# Path to your 2025proj folder
proj_folder = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj"

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(proj_folder, "*.csv"))

# Read all CSVs into DataFrames
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    # Standardize column names
    df.columns = [col.strip().upper() for col in df.columns]
    # Always keep PLAYER column, rename if needed
    if 'PLAYER' not in df.columns:
        if 'Player' in df.columns:
            df.rename(columns={'Player': 'PLAYER'}, inplace=True)
        elif 'player' in df.columns:
            df.rename(columns={'player': 'PLAYER'}, inplace=True)
    # Some DSTs may not have a team, fill with empty string
    if 'TEAM' not in df.columns:
        df['TEAM'] = ""
    dfs.append(df)

# Merge all DataFrames on PLAYER (and TEAM, if you want to keep team info)
from functools import reduce

def merge_fillna(left, right):
    # Merge on PLAYER, outer join
    merged = pd.merge(left, right, on=['PLAYER'], how='outer', suffixes=('', '_dup'))
    # Remove duplicate columns from merge (e.g., TEAM_dup)
    for col in merged.columns:
        if col.endswith('_dup'):
            merged.drop(columns=col, inplace=True)
    return merged

combined = reduce(merge_fillna, dfs)

# Fill all NaN with 0 (as requested)
combined = combined.fillna(0)

# Save to CSV
output_path = os.path.join(proj_folder, "FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED.csv")
combined.to_csv(output_path, index=False)
print(f"Combined CSV saved to: {output_path}")