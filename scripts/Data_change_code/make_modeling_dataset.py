import os
import pandas as pd

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"
out_file = os.path.join(base_dir, "modeling_dataset.csv")

model_cols = [
    "Player", "Year", "Position", "Team", "Games Played", "Fantasy Points", "PPG",
    "Targets", "Receptions", "Carries", "Touchdowns", "Air Yards", "YAC",
    "Routes Run", "Red Zone Touches", "Goal Line Touches"
]

col_map = {
    "Player": ["Player", "player_name", "passer_player_name"],
    "Year": ["Year", "year", "Season year"],
    "Position": ["Position", "position"],
    "Team": ["posteam", "Team", "team", "Posteam"],
    "Games Played": ["Games Played (Advanced)", "Games Played", "Games Played (Basic)"],
    "Fantasy Points": ["Fantasy Points"],
    "PPG": ["Fantasy Points/Game", "Fantasy Points Per Game"],
    "Targets": ["Targets (Advanced)", "targets", "Targets"],
    "Receptions": ["Receptions (Advanced)", "receptions", "Receptions"],
    "Carries": ["Rushing Attempts (Advanced)", "Rushing Attempts", "Carries"],
    "Touchdowns": [
        "TDs", "Touchdowns", "Receiving TD (Basic)", "Receiving TD", "Rushing TD (Basic)", "Rushing TD", "Passing TD"
    ],
    "Air Yards": ["Air Yards"],
    "YAC": ["YAC", "yac", "Yards After Catch", "Yards After Catch (YAC)"],
    "Routes Run": ["routes_run", "Routes Run", "season_routes", "Routes run (routes)"],
    "Red Zone Touches": ["redzone_touches", "Red Zone Touches"],
    "Goal Line Touches": ["goal_line_touches", "Goal Line Touches"]
}

def find_column(df, names):
    for name in names:
        if name in df.columns:
            return name
    return None

dfs = []
for pos in ["rb", "wr", "te", "qb"]:
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
    new_data = {}
    for out_col, possible_names in col_map.items():
        col = find_column(df, possible_names)
        if col:
            new_data[out_col] = df[col]
        else:
            new_data[out_col] = ""
    # Touchdowns: sum receiving + rushing + passing if present (for QBs)
    if pos == "qb":
        # Always use Series for missing columns
        n = len(df)
        passing_td = pd.to_numeric(df["Passing TD"], errors='coerce').fillna(0) if "Passing TD" in df.columns else pd.Series([0]*n)
        rushing_td = pd.to_numeric(df["Rushing TD (Basic)"], errors='coerce').fillna(0) if "Rushing TD (Basic)" in df.columns else pd.Series([0]*n)
        new_data["Touchdowns"] = passing_td + rushing_td
        # Carries: use Rushing Attempts
        carries_col = find_column(df, ["Rushing Attempts (Advanced)", "Rushing Attempts"])
        if carries_col:
            new_data["Carries"] = df[carries_col]
    else:
        # For others, sum receiving + rushing if both present
        if "Receiving TD (Basic)" in df.columns and "Rushing TD (Basic)" in df.columns:
            new_data["Touchdowns"] = (
                pd.to_numeric(df["Receiving TD (Basic)"], errors='coerce').fillna(0) +
                pd.to_numeric(df["Rushing TD (Basic)"], errors='coerce').fillna(0)
            )
    dfs.append(pd.DataFrame(new_data))

if dfs:
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined[model_cols]
    combined.to_csv(out_file, index=False)
    print(f"Created {out_file}")
else:
    print("No data found to combine.")