import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

desired_order = [
    "Rank",
    "Player",
    "Fantasy Points",
    "Fantasy Points/Game",
    "Passing TD",
    "Interceptions",
    "Passing Yards (Advanced)",
    "Completion % (Advanced)",
    "Yards/Attempt (Advanced)",
    "CPOE",
    "Completions (Advanced)",
    "Pass Attempts (Advanced)",
    "Air Yards",
    "Air Yards/Attempt",
    "Completions 10+ Yards",
    "Completions 20+ Yards",
    "Completions 30+ Yards",
    "Completions 40+ Yards",
    "Completions 50+ Yards",
    "Red Zone Attempts",
    "QB Rating",
    "Pocket Time",
    "Sacks (Advanced)",
    "pressure_to_sack",
    "QB Hits/Knockdowns",
    "QB Hurries",
    "Blitzes Faced",
    "Poor Throws",
    "Receiver Drops",
    "Rushing TD",
    "Rushing Yards",
    "Rushing Attempts",
    "Fumbles Lost",
    "Games Played (Advanced)",
    "player_id",
    "Year",
    "pressures"
]

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file, on_bad_lines='skip')  # pandas ≥1.3
        ordered_cols = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
        df = df[ordered_cols]
        df.to_csv(csv_file, index=False)
        print(f"Reordered: {csv_file}")
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")