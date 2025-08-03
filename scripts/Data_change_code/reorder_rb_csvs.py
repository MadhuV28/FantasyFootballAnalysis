import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

desired_order = [
    "Rank",
    "Player",
    "Fantasy Points",
    "Fantasy Points/Game",
    "Rushing Yards",
    "Rushing Attempts",
    "Rushing TD",
    "Fumbles Lost",
    "Red Zone Attempts",
    "Completions (Advanced)",
    "Passing Yards (Advanced)",
    "Completion % (Advanced)",
    "Completions 10+ Yards",
    "Completions 20+ Yards",
    "Completions 30+ Yards",
    "Completions 40+ Yards",
    "Completions 50+ Yards",
    "Yards/Attempt (Advanced)",
    "CPOE",
    "Air Yards",
    "Air Yards/Attempt",
    "Receiver Drops",
    "Poor Throws",
    "QB Rating",
    "Pocket Time",
    "Sacks (Advanced)",
    "pressure_to_sack",
    "QB Hits/Knockdowns",
    "QB Hurries",
    "Blitzes Faced",
    "Interceptions",
    "Passing TD",
    "Games Played (Advanced)",
    "Position",
    "player_id",
    "Year",
    "pressures"
]

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    df = pd.read_csv(csv_file)
    # Only keep columns that exist in the file
    ordered_cols = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[ordered_cols]
    df.to_csv(csv_file, index=False)
    print(f"Reordered: {csv_file}")