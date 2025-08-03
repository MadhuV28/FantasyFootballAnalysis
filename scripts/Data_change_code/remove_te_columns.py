import os
import pandas as pd
import glob

te_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/te"

cols_to_remove = [
    "Receptions (Basic)",
    "Targets (Basic)",
    "Receiving Yards (Basic)",
    "Yards/Reception (Basic)",
    "Longest Reception",
    "Receptions 20+ Yards.1",
    "Games Played (Basic)",
    "player_name_std",
    "receiver_player_id",
    "receiver_player_name",
    "receiving_yards"
]

for csv_file in glob.glob(os.path.join(te_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Removed columns: {csv_file}")