import pandas as pd

csv_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/fantasy_skill_positions.csv"

desired_order = [
    "Player",
    "Year",
    "Position",
    "Team",
    "Games Played",
    "Fantasy Points",
    "Fantasy PPG",
    "Targets",
    "Receptions",
    "Carries",  # This will be mapped from "Rushing Attempts/Yards"
    "TDs",
    "Air Yards",
    "YAC",
    "Routes Run",
    "Red Zone Touches",
    "Goal Line Touches"
]

df = pd.read_csv(csv_path)

# If "Carries" doesn't exist, extract from "Rushing Attempts/Yards"
if "Carries" not in df.columns and "Rushing Attempts/Yards" in df.columns:
    df["Carries"] = df["Rushing Attempts/Yards"].astype(str).str.split("/").str[0]

# Add missing columns as empty if needed
for col in desired_order:
    if col not in df.columns:
        df[col] = ""

df = df[desired_order]
df.to_csv(csv_path, index=False)
print("Reordered columns in fantasy_skill_positions.csv.")