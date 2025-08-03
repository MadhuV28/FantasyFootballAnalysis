import os
import glob
import pandas as pd

# Folder containing your yearly team context CSVs
context_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/team_context"
out_file = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/team_context_all_years.csv"

# Columns to keep and standardize
keep_cols = ["Team", "Year", "Total_Plays", "RedZone_Plays", "Team_AirYards"]

dfs = []
for file in glob.glob(os.path.join(context_dir, "*.csv")):
    df = pd.read_csv(file)
    # Try to standardize column names
    df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]
    # Rename columns if needed
    rename_map = {}
    for col in df.columns:
        if col.lower() in ["team", "posteam"]:
            rename_map[col] = "Team"
        elif col.lower() in ["year", "season"]:
            rename_map[col] = "Year"
        elif "total" in col.lower() and "play" in col.lower():
            rename_map[col] = "Total_Plays"
        elif "redzone" in col.lower() and "play" in col.lower():
            rename_map[col] = "RedZone_Plays"
        elif "air" in col.lower() and "yard" in col.lower():
            rename_map[col] = "Team_AirYards"
    df = df.rename(columns=rename_map)
    # Only keep the columns we want
    for col in keep_cols:
        if col not in df.columns:
            df[col] = ""
    dfs.append(df[keep_cols])

if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    merged = merged[keep_cols]
    merged.to_csv(out_file, index=False)
    print(f"Created {out_file}")
else:
    print("No team context files found.")