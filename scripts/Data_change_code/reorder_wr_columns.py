import os
import pandas as pd
import glob

wr_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/wr"

desired_order = [
    "Rank",
    "Player",
    "Fantasy Points",
    "Fantasy Points/Game",
    "Receptions (Advanced)",
    "Targets (Advanced)",
    "Target Share %",
    "Catchable Targets",
    "Drops",
    "Receiving Yards (Advanced)",
    "Yards/Reception (Advanced)",
    "Air Yards",
    "Air Yards/Reception",
    "Yards Before Catch",
    "Yards Before Catch/Reception",
    "Yards After Catch",
    "Yards After Catch/Reception",
    "Yards After Contact",
    "Yards After Contact/Reception",
    "Broken Tackles",
    "Receiving TD (Basic)",
    "Receptions 10+ Yards",
    "Receptions 20+ Yards",
    "Receptions 30+ Yards",
    "Receptions 40+ Yards",
    "Receptions 50+ Yards",
    "Longest Reception (Advanced)",
    "Red Zone Targets",
    "routes_run",
    "yprr",
    "TPRR",
    "Rushing Attempts",
    "Rushing Yards",
    "Rushing TD",
    "Fumbles Lost",
    "redzone_touches",
    "goal_line_touches",
    "Games Played (Advanced)",
    "Rostered %",
    "Year",
    "Position",
    "posteam",
    "player_id",
    "player_name"
]

for csv_file in glob.glob(os.path.join(wr_dir, "*.csv")):
    df = pd.read_csv(csv_file)
    # Prefer advanced columns over basic, drop duplicates
    if "Receptions (Advanced)" in df.columns and "Receptions (Basic)" in df.columns:
        df = df.drop(columns=["Receptions (Basic)"])
    if "Targets (Advanced)" in df.columns and "Targets (Basic)" in df.columns:
        df = df.drop(columns=["Targets (Basic)"])
    if "Receiving Yards (Advanced)" in df.columns and "Receiving Yards (Basic)" in df.columns:
        df = df.drop(columns=["Receiving Yards (Basic)"])
    if "Yards/Reception (Advanced)" in df.columns and "Yards/Reception (Basic)" in df.columns:
        df = df.drop(columns=["Yards/Reception (Basic)"])
    if "Longest Reception (Advanced)" in df.columns and "Longest Reception" in df.columns:
        df = df.drop(columns=["Longest Reception"])
    # Drop duplicate "Receptions 20+ Yards.1"
    if "Receptions 20+ Yards.1" in df.columns:
        df = df.drop(columns=["Receptions 20+ Yards.1"])
    # Only keep columns that exist in the file
    ordered_cols = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[ordered_cols]
    df.to_csv(csv_file, index=False)
    print(f"Reordered: {csv_file}")