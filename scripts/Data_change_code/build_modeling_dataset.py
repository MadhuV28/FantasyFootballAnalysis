import os
import pandas as pd
import re

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"
team_context_path = os.path.join(base_dir, "team_context_all_years.csv")
out_file = os.path.join(base_dir, "modeling_dataset.csv")

# Standard columns for modeling
model_cols = [
    "Player", "Year", "Position", "Team", "Games Played", "Fantasy Points", "PPG",
    "Targets", "Receptions", "Carries", "Touchdowns", "Air Yards", "YAC",
    "Routes Run", "Red Zone Touches", "Goal Line Touches",
    # Derived metrics:
    "Fantasy Points Per Touch", "Points Per Opportunity", "Opportunity Share",
    "TPRR", "YPRR"
]

# Load team context
team_context = pd.read_csv(team_context_path)
team_context["Year"] = pd.to_numeric(team_context["Year"], errors="coerce")

def safe_div(n, d):
    try:
        return n / d if d != 0 else None
    except Exception:
        return None

# Extract team from player string (customize regex as needed)
def extract_team(player_str):
    match = re.search(r'\[(.*?)\]', player_str)
    return match.group(1) if match else None

dfs = []
for pos in ["rb", "wr", "te", "qb"]:
    csv_path = os.path.join(base_dir, f"{pos}_all_years.csv")
    if not os.path.exists(csv_path):
        continue
    df = pd.read_csv(csv_path)
    # Remove description/header rows if present
    if isinstance(df.iloc[0, 0], str) and "player" in df.columns[0].lower():
        df = df[df[df.columns[0]].str.lower() != "player"]
    if isinstance(df.iloc[0, 0], str) and "fantasy" in df.iloc[0, 0].lower():
        df = df.iloc[1:]
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    # Rename for merge
    rename_map = {}
    for col in df.columns:
        if col.lower() in ["team", "posteam", "team abbreviation"]:
            rename_map[col] = "Team"
        elif col.lower() in ["year", "season", "season year"]:
            rename_map[col] = "Year"
    df = df.rename(columns=rename_map)
    # Ensure Team and Year columns exist
    if "Team" not in df.columns or "Year" not in df.columns:
        print(f"Skipping {csv_path}: missing Team or Year column after renaming.")
        continue
    # If Team column is missing, extract from Player
    if "Team" not in df.columns and "Player" in df.columns:
        df["Team"] = df["Player"].apply(lambda x: extract_team(x))
    # Merge with team context
    df = df.merge(team_context, on=["Team", "Year"], how="left")
    # Convert relevant columns to numeric
    for col in [
        "Fantasy Points", "Carries", "Receptions", "Targets", "Routes Run",
        "Receiving Yards", "Red Zone Touches", "Air Yards", "YAC", "Total_Plays"
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    # Derived metrics
    df["Fantasy Points Per Touch"] = df.apply(lambda row: safe_div(row.get("Fantasy Points", 0), row.get("Carries", 0) + row.get("Receptions", 0)), axis=1)
    df["Points Per Opportunity"] = df.apply(lambda row: safe_div(row.get("Fantasy Points", 0), row.get("Carries", 0) + row.get("Targets", 0)), axis=1)
    df["Opportunity Share"] = df.apply(lambda row: safe_div(row.get("Carries", 0) + row.get("Targets", 0), row.get("Total_Plays", 0)), axis=1)
    df["TPRR"] = df.apply(lambda row: safe_div(row.get("Targets", 0), row.get("Routes Run", 0)), axis=1)
    df["YPRR"] = df.apply(lambda row: safe_div(row.get("Receiving Yards", 0), row.get("Routes Run", 0)), axis=1)
    # Standardize output columns
    for col in model_cols:
        if col not in df.columns:
            df[col] = ""
    dfs.append(df[model_cols])

# Combine all positions
if dfs:
    modeling_df = pd.concat(dfs, ignore_index=True)
    modeling_df.to_csv(out_file, index=False)
    print(f"Created {out_file} with derived metrics.")
else:
    print("No data found to combine.")