import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

cols_to_remove = [
    "Longest Run",
    "Rushing Attempts (Basic)",
    "Rushing Yards (Basic)",
    "Receptions (Basic)",
    "Targets (Basic)",
    "targets",
    "Receiving Yards (Basic)",
    "receiving_yards",
    "Runs 20+ Yards",
    "Games Played (Basic)",
    "player_name_std",
    "player_name",
    "receiver_player_id",
    "receiver_player_name",
    "receiver_player_id_yprr",
    "receiver_player_name_yprr",
    "receiver_player_id_routes",
    "receiver_player_name_routes"
]

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue
    # Handle receiving yards: keep only one version
    if "Receiving Yards (Basic)" in df.columns and "receiving_yards" in df.columns:
        df = df.drop(columns=["receiving_yards"])
        cols_to_remove = [col for col in cols_to_remove if col != "Receiving Yards (Basic)"]
    elif "receiving_yards" in df.columns:
        cols_to_remove = [col for col in cols_to_remove if col != "receiving_yards"]
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Removed columns: {csv_file}")