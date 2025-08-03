import pandas as pd
import os

# === Paths ===
base_dir = "DataInfo/pos_combined_year"
team_context_path = os.path.join(base_dir, "team_context_all_years.csv")
positions = ["qb_modeling.csv", "rb_modeling.csv", "wr_modeling.csv", "te_modeling.csv"]

# === Load team context ===
team_context = pd.read_csv(team_context_path).rename(columns={
    "Team": "Team",
    "Year": "Year",
    "Total_Plays": "Team_Total_Plays"
})

# === Load and merge modeling datasets ===
dfs = []
for pos_file in positions:
    df = pd.read_csv(os.path.join(base_dir, pos_file))
    dfs.append(df)
modeling = pd.concat(dfs, ignore_index=True)

# === Merge team context ===
modeling = modeling.merge(team_context, how="left", left_on=["Team", "Year"], right_on=["Team", "Year"])

# === Ensure numeric columns ===
for col in [
    "Carries", "Receptions", "Targets", "Fantasy Points", "Routes Run", "Air Yards",
    "Red Zone Touches", "Goal Line Touches", "Team_Total_Plays"
]:
    if col in modeling.columns:
        modeling[col] = pd.to_numeric(modeling[col], errors="coerce").fillna(0)

# === Calculate Derived Metrics ===
modeling["Touches"] = modeling["Carries"] + modeling["Receptions"]
modeling["Opportunities"] = modeling["Carries"] + modeling["Targets"]

modeling["FantasyPointsPerTouch"] = modeling["Fantasy Points"] / modeling["Touches"].replace(0, pd.NA)
modeling["PointsPerOpportunity"] = modeling["Fantasy Points"] / modeling["Opportunities"].replace(0, pd.NA)
modeling["OpportunityShare"] = modeling["Opportunities"] / modeling["Team_Total_Plays"].replace(0, pd.NA)
modeling["TPRR"] = modeling["Targets"] / modeling["Routes Run"].replace(0, pd.NA)
modeling["YPRR"] = modeling["Air Yards"] / modeling["Routes Run"].replace(0, pd.NA)
modeling["AirYardsShare"] = modeling["Air Yards"] / modeling.groupby(["Year", "Team"])["Air Yards"].transform("sum")

# Red zone share
modeling["RedZoneShare"] = modeling["Red Zone Touches"] / modeling.groupby(["Year", "Team"])["Red Zone Touches"].transform("sum")
modeling["GoalLineShare"] = modeling["Goal Line Touches"] / modeling.groupby(["Year", "Team"])["Goal Line Touches"].transform("sum")

# === Save final dataset ===
output_path = "DataInfo/modeling_final.csv"
modeling.to_csv(output_path, index=False)

print(f"Base modeling dataset saved to {output_path}")
