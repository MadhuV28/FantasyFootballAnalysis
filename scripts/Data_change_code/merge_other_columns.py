import os
import pandas as pd
import glob

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo"
positions = ["qb", "rb", "wr", "te"]
other_dir = os.path.join(base_dir, "other")

# Get all position files
position_files = []
for pos in positions:
    pos_dir = os.path.join(base_dir, pos)
    position_files += glob.glob(os.path.join(pos_dir, "*.csv"))

# Get all "other" files (recursively)
other_files = []
for root, _, files in os.walk(other_dir):
    for fname in files:
        if fname.endswith(".csv"):
            other_files.append(os.path.join(root, fname))

for pos_file in position_files:
    df_pos = pd.read_csv(pos_file, low_memory=False)
    for other_file in other_files:
        df_other = pd.read_csv(other_file)
        # Only keep columns from "other" that are not player_name_std
        other_cols = [col for col in df_other.columns if col != "player_name_std"]
        # Only merge columns, not rows
        if "player_name_std" in df_pos.columns and "player_name_std" in df_other.columns:
            df_pos = df_pos.merge(
                df_other[["player_name_std"] + other_cols],
                on="player_name_std",
                how="left",
                suffixes=('', f'_{os.path.splitext(os.path.basename(other_file))[0]}')
            )
    df_pos.to_csv(pos_file, index=False)
    print(f"Merged columns from 'other' into {pos_file}")