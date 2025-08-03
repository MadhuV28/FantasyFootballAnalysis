import os
import glob
import pandas as pd

context_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/team_context"
out_file = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/team_context_all_years.csv"

dfs = []
for file in glob.glob(os.path.join(context_dir, "*.csv")):
    df = pd.read_csv(file)
    # Skip description row if present
    if isinstance(df.iloc[0, 0], str) and "season" in df.iloc[0, 0].lower():
        df = df.iloc[1:]
    df = df.rename(columns={
        "season": "Year",
        "posteam": "Team",
        "plays_per_game": "Plays_Per_Game"
    })
    # Estimate total plays (assume 16 games before 2021, 17 games 2021+)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Plays_Per_Game"] = pd.to_numeric(df["Plays_Per_Game"], errors="coerce")
    df["Total_Plays"] = df.apply(
        lambda row: row["Plays_Per_Game"] * (17 if row["Year"] >= 2021 else 16), axis=1
    )
    df["RedZone_Plays"] = ""
    df["Team_AirYards"] = ""
    dfs.append(df[["Team", "Year", "Total_Plays", "RedZone_Plays", "Team_AirYards"]])

if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    merged = merged[["Team", "Year", "Total_Plays", "RedZone_Plays", "Team_AirYards"]]
    merged = merged.dropna(subset=["Team", "Year"])
    merged = merged[merged["Team"] != ""]
    merged.to_csv(out_file, index=False)
    print(f"Created {out_file}")
else:
    print("No team context files found.")