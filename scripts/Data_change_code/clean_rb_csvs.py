import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

cols_to_remove = [
    "Interceptions",
    "Passing TD",
    "Passing Yards (Advanced)",
    "Completion % (Advanced)",
    "Yards/Attempt (Advanced)",
    "CPOE",
    "Air Yards",
    "Air Yards/Attempt",
    "QB Rating",
    "Pocket Time",
    "Sacks (Advanced)",
    "pressure_to_sack",
    "QB Hits/Knockdowns",
    "QB Hurries",
    "Blitzes Faced",
    "Poor Throws",
    "pressures"
]

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    df = pd.read_csv(csv_file)
    # Only drop columns that exist in the file
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Cleaned: {csv_file}")