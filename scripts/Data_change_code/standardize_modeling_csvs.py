import os
import pandas as pd
import re

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"
positions = ["rb", "wr", "te", "qb"]
standard_cols = [
    "Player", "Year", "Position", "Team", "Games Played", "Fantasy Points", "PPG",
    "Targets", "Receptions", "Carries", "Touchdowns", "Air Yards", "YAC",
    "Routes Run", "Red Zone Touches", "Goal Line Touches"
]

def extract_team(player):
    m = re.search(r'\((\w+)\)', str(player))
    return m.group(1) if m else ""

for pos in positions:
    in_path = os.path.join(base_dir, f"{pos}_all_years.csv")
    out_path = os.path.join(base_dir, f"{pos}_modeling.csv")
    if not os.path.exists(in_path):
        continue
    df = pd.read_csv(in_path)

    # Position-specific column mapping
    if pos == "rb":
        col_map = {
            "Player": "Player",
            "Year": "Year",
            "Position": "Position",
            "posteam": "Team",
            "Games Played (Advanced)": "Games Played",
            "Fantasy Points": "Fantasy Points",
            "Fantasy Points/Game": "PPG",
            "Targets (Advanced)": "Targets",
            "Receptions (Advanced)": "Receptions",
            "Rushing Attempts (Advanced)": "Carries",
            # Touchdowns = Rushing TD (Basic) + Receiving TD (Basic)
            "Rushing TD (Basic)": "Rushing TD (Basic)",
            "Receiving TD (Basic)": "Receiving TD (Basic)",
            "Air Yards": "Air Yards",  # RBs usually don't have this, will fill blank
            "yac": "YAC",
            "routes_run": "Routes Run",  # RBs usually don't have this, will fill blank
            "redzone_touches": "Red Zone Touches",
            "goal_line_touches": "Goal Line Touches"
        }
    elif pos in ["wr", "te"]:
        col_map = {
            "Player": "Player",
            "Year": "Year",
            "Position": "Position",
            "posteam": "Team",
            "Games Played (Advanced)": "Games Played",
            "Fantasy Points": "Fantasy Points",
            "Fantasy Points/Game": "PPG",
            "Targets (Advanced)": "Targets",
            "Receptions (Advanced)": "Receptions",
            "Rushing Attempts (Advanced)": "Carries",  # usually blank for WR/TE
            "Receiving TD (Basic)": "Touchdowns",
            "Air Yards": "Air Yards",
            "yac": "YAC",
            "routes_run": "Routes Run",
            "redzone_touches": "Red Zone Touches",
            "goal_line_touches": "Goal Line Touches"
        }
    elif pos == "qb":
        col_map = {
            "Player": "Player",
            "Year": "Year",
            "Position": "Position",
            # Team will be extracted from Player
            "Games Played (Advanced)": "Games Played",
            "Fantasy Points": "Fantasy Points",
            "Fantasy Points/Game": "PPG",
            # No Targets/Receptions for QB
            "Rushing Attempts": "Carries",
            "Passing TD": "Passing TD",
            "Rushing TD": "Rushing TD",
            "Air Yards": "Air Yards",
            "yac": "YAC",  # usually blank for QB
            "routes_run": "Routes Run",  # usually blank for QB
            "Red Zone Attempts": "Red Zone Touches",  # not exactly the same, but closest
            "goal_line_touches": "Goal Line Touches"  # usually blank for QB
        }

    # Build standardized DataFrame
    out_df = pd.DataFrame(columns=standard_cols)
    for std_col in standard_cols:
        # Find the source column for this standardized column
        src_col = None
        for k, v in col_map.items():
            if v == std_col and k in df.columns:
                src_col = k
                break
        if src_col:
            out_df[std_col] = df[src_col]
        elif std_col == "Team" and pos == "qb":
            out_df[std_col] = df["Player"].apply(extract_team)
        elif std_col == "Touchdowns" and pos == "rb":
            # RB: sum Rushing TD (Basic) + Receiving TD (Basic)
            rush = pd.to_numeric(df.get("Rushing TD (Basic)", 0), errors="coerce").fillna(0)
            rec = pd.to_numeric(df.get("Receiving TD (Basic)", 0), errors="coerce").fillna(0)
            out_df[std_col] = rush + rec
        elif std_col == "Touchdowns" and pos == "qb":
            # QB: sum Passing TD + Rushing TD
            passing = pd.to_numeric(df.get("Passing TD", 0), errors="coerce").fillna(0)
            rushing = pd.to_numeric(df.get("Rushing TD", 0), errors="coerce").fillna(0)
            out_df[std_col] = passing + rushing
        else:
            out_df[std_col] = ""

    out_df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")