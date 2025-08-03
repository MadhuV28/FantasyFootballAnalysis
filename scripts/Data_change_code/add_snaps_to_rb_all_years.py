import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"
all_years_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years.csv"
output_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_snaps.csv"

# Load the all-years file
all_years = pd.read_csv(all_years_path)

# Build a mapping from (Player, Year) to relevent_snaps_played
snaps_map = {}

for file in glob.glob(os.path.join(rb_dir, "*RB_merged.csv")):
    df = pd.read_csv(file)
    # Try to find the correct column name (case-insensitive)
    snaps_col = next((c for c in df.columns if c.strip().lower() == "relevent_snaps_played"), None)
    player_col = next((c for c in df.columns if c.strip().lower() == "player"), None)
    year_col = next((c for c in df.columns if "year" in c.strip().lower()), None)
    if not (snaps_col and player_col and year_col):
        continue
    for _, row in df.iterrows():
        key = (str(row[player_col]).strip(), str(row[year_col]).strip())
        snaps_map[key] = row[snaps_col]

# Add the column to all_years
all_years["relevent_snaps_played"] = all_years.apply(
    lambda row: snaps_map.get((str(row["Player"]).strip(), str(row["Year"]).strip()), ""),
    axis=1
)

all_years.to_csv(output_path, index=False)
print(f"Wrote {output_path}")