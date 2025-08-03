import os
import pandas as pd
import glob

wr_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/wr"

cols_to_remove = [
    "Games Played (Basic)",
    "receiving_yards",
    "targets",
    "player_name_std",
    "receiver_player_id",
    "receiver_player_name",
    "player_name",
    "Rostered %",
    "redzone_touches",
    "goal_line_touches",
    "Rushing Attempts",
    "Rushing Yards",
    "Rushing TD",
    "Fumbles Lost"
]

for csv_file in glob.glob(os.path.join(wr_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue
    df