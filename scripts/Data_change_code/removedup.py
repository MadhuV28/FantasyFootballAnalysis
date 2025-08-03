import os
import pandas as pd
import glob

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo"
positions = ["qb", "rb", "wr", "te"]
other_dir = os.path.join(base_dir, "other")

# Remove files in position folders that don't have "merg" in the name
for pos in positions:
    pos_dir = os.path.join(base_dir, pos)
    for fname in os.listdir(pos_dir):
        if "merg" not in fname.lower() and fname.endswith(".csv"):
            fpath = os.path.join(pos_dir, fname)
            if os.path.isfile(fpath):
                os.remove(fpath)
                print(f"Deleted: {fpath}")

# Collect all player_name_std from remaining position files
all_players = set()
for pos in positions:
    pos_dir = os.path.join(base_dir, pos)
    for fname in glob.glob(os.path.join(pos_dir, "*.csv")):
        df = pd.read_csv(fname)
        if "player_name_std" in df.columns:
            all_players.update(df["player_name_std"].dropna().astype(str).str.strip())

# Filter each CSV in DataInfo/other and subfolders
for root, _, files in os.walk(other_dir):
    for fname in files:
        if fname.endswith(".csv"):
            fpath = os.path.join(root, fname)
            df = pd.read_csv(fpath)
            if "player_name_std" in df.columns:
                before = len(df)
                df = df[df["player_name_std"].astype(str).str.strip().isin(all_players)]
                after = len(df)
                df.to_csv(fpath, index=False)
                print(f"Filtered {fpath}: {before} -> {after} rows")