import os
import pandas as pd

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"
out_file = os.path.join(base_dir, "fantasy_skill_positions.csv")

# Mapping of your desired columns to possible column names in source files
col_map = {
    "Player": ["Player", "player_name"],
    "Position": ["Position", "position"],
    "Year": ["Year", "year", "Season year"],
    "Fantasy Points": ["Fantasy Points"],
    "Fantasy PPG": ["Fantasy Points/Game", "Fantasy Points Per Game"],
    "Games Played": ["Games Played (Advanced)", "Games Played", "Games Played (Basic)"],
    "Team": ["posteam", "Team", "team", "Posteam"],
    "Red Zone Touches": ["redzone_touches", "Red Zone Touches"],
    "Targets": ["Targets (Advanced)", "targets", "Targets"],
    "Receptions": ["Receptions (Advanced)", "receptions", "Receptions"],
    "Receiving Yards": ["Receiving Yards (Advanced)", "receiving_yards", "Receiving Yards"],
    "TDs": ["Receiving TD (Basic)", "Receiving TD", "Receiving touchdowns (basic)", "Rushing TD (Basic)", "Rushing TD", "TD"],
    "Rushing Attempts/Yards": ["Rushing Attempts (Advanced)", "Rushing Attempts", "Rushing Yards (Advanced)", "Rushing Yards"]
}

def find_column(df, names):
    for name in names:
        if name in df.columns:
            return name
    return None

dfs = []
for pos in ["rb", "wr", "te"]:
    csv_path = os.path.join(base_dir, f"{pos}_all_years.csv")
    if not os.path.exists(csv_path):
        continue
    df = pd.read_csv(csv_path)
    # Skip description row if present
    if len(df) > 1 and (
        "fantasy" in str(df.iloc[1, 0]).lower()
        or "ranking" in str(df.iloc[1, 0]).lower()
        or "player name" in str(df.iloc[1, 0]).lower()
    ):
        df = df.iloc[2:].reset_index(drop=True)
    # Build new DataFrame with only the mapped columns
    new_data = {}
    for out_col, possible_names in col_map.items():
        col = find_column(df, possible_names)
        if col:
            new_data[out_col] = df[col]
        else:
            new_data[out_col] = ""
    # For TDs, prefer receiving TDs, then rushing TDs, then total TDs
    if "Receiving TD (Basic)" in df.columns and "Rushing TD (Basic)" in df.columns:
        new_data["TDs"] = (
            pd.to_numeric(df["Receiving TD (Basic)"], errors='coerce').fillna(0) +
            pd.to_numeric(df["Rushing TD (Basic)"], errors='coerce').fillna(0)
        )
    # For Rushing Attempts/Yards, combine if both present
    rush_att = find_column(df, ["Rushing Attempts (Advanced)", "Rushing Attempts"])
    rush_yds = find_column(df, ["Rushing Yards (Advanced)", "Rushing Yards"])
    if rush_att and rush_yds:
        new_data["Rushing Attempts/Yards"] = df[rush_att].astype(str) + "/" + df[rush_yds].astype(str)
    elif rush_att:
        new_data["Rushing Attempts/Yards"] = df[rush_att]
    elif rush_yds:
        new_data["Rushing Attempts/Yards"] = df[rush_yds]
    dfs.append(pd.DataFrame(new_data))

# Combine all and drop duplicates
if dfs:
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined[
        ["Player", "Position", "Year", "Fantasy Points", "Fantasy PPG", "Games Played", "Team",
         "Red Zone Touches", "Targets", "Receptions", "Receiving Yards", "TDs", "Rushing Attempts/Yards"]
    ]
    combined.to_csv(out_file, index=False)
    print(f"Created {out_file}")
else:
    print("No data found to combine.")