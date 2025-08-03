import os
import pandas as pd
import glob

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo"
positions = ["qb", "rb", "wr", "te"]

for pos in positions:
    pos_dir = os.path.join(base_dir, pos)
    for csv_file in glob.glob(os.path.join(pos_dir, "*.csv")):
        df = pd.read_csv(csv_file, low_memory=False)
        # Remove duplicate rows based on player_name_std column
        before = len(df)
        if 'player_name_std' in df.columns:
            df = df.drop_duplicates(subset=['player_name_std'])
        elif 'player' in df.columns:
            df = df.drop_duplicates(subset=['player'])
        after = len(df)
        df.to_csv(csv_file, index=False)
        print(f"Removed duplicates in {csv_file}: {before} -> {after} rows")

# Use the correct path for the file
qb_file = os.path.join(base_dir, "qb", "2015QB_merged.csv")
df = pd.read_csv(qb_file)

# Columns to drop
cols_to_drop = [
    'Completions',
    'Pass Attempts (Basic)',
    'Completion % (Basic)',
    'Passing Yards (Basic)',
    'Sacks (Basic)',
    'passer_player_name',
    'season',
    'passer_player_id'
]

# Drop columns
df = df.drop(columns=cols_to_drop)

# Save back to CSV
df.to_csv(os.path.join(base_dir, "qb", "2015QB_merged_cleaned.csv"), index=False)