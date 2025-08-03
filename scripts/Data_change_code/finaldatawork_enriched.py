import pandas as pd
import os

# === Paths ===
base_dir = "DataInfo/pos_combined_year"
team_context_path = os.path.join(base_dir, "team_context_all_years.csv")

modeling_files = {
    "QB": "qb_modeling.csv",
    "RB": "rb_modeling.csv",
    "WR": "wr_modeling.csv",
    "TE": "te_modeling.csv"
}

all_years_files = {
    "QB": "qb_all_years.csv",
    "RB": "rb_all_years.csv",
    "WR": "wr_all_years.csv",
    "TE": "te_all_years.csv"
}

# === Load team context ===
team_context = pd.read_csv(team_context_path).rename(columns={
    "Team": "Team",
    "Year": "Year",
    "Total_Plays": "Team_Total_Plays"
})

# === Load base modeling datasets ===
dfs = []
for pos, file in modeling_files.items():
    df = pd.read_csv(os.path.join(base_dir, file))
    df["Position"] = pos  # Make sure position is explicit
    dfs.append(df)
modeling = pd.concat(dfs, ignore_index=True)

# === Merge with team context ===
modeling = modeling.merge(team_context, how="left", left_on=["Team", "Year"], right_on=["Team", "Year"])

# === Load advanced all_years datasets and merge ===
for pos, file in all_years_files.items():
    adv = pd.read_csv(os.path.join(base_dir, file))
    adv["Position"] = pos
    # Align column names (Player vs player_name etc.)
    if "player_name" in adv.columns:
        adv.rename(columns={"player_name": "Player"}, inplace=True)
    if "posteam" in adv.columns:
        adv.rename(columns={"posteam": "Team"}, inplace=True)
    # Merge all columns except duplicates of existing modeling ones
    cols_to_use = [c for c in adv.columns if c not in modeling.columns or c in ["Player", "Year", "Team", "Position"]]
    
    # Ensure no duplicate columns in selection (preserve order)
    merge_cols = list(dict.fromkeys(cols_to_use + ["Player", "Year", "Position"]))

    # Remove columns from adv_merge that are already in modeling (except merge keys)
    merge_keys = ["Player", "Year", "Position"]
    existing_cols = set(modeling.columns)
    cols_final = merge_keys + [col for col in merge_cols if col not in existing_cols or col in merge_keys]

    adv_unique = adv.loc[:, ~adv.columns.duplicated()]
    adv_merge = adv_unique[cols_final]
    adv_merge = adv_merge.loc[:, ~adv_merge.columns.duplicated()]  # Remove any duplicates after selection
    modeling = modeling.merge(adv_merge, how="left", on=merge_keys)

# === Ensure numeric columns for derived metrics ===
for col in [
    "Carries", "Receptions", "Targets", "Fantasy Points", "Routes Run", "Air Yards",
    "Red Zone Touches", "Goal Line Touches", "Team_Total_Plays"
]:
    if col in modeling.columns:
        modeling[col] = pd.to_numeric(modeling[col], errors="coerce").fillna(0)

# === Derived Metrics ===
modeling["Touches"] = modeling["Carries"] + modeling["Receptions"]
modeling["Opportunities"] = modeling["Carries"] + modeling["Targets"]

modeling["FantasyPointsPerTouch"] = modeling["Fantasy Points"] / modeling["Touches"].replace(0, pd.NA)
modeling["PointsPerOpportunity"] = modeling["Fantasy Points"] / modeling["Opportunities"].replace(0, pd.NA)
modeling["OpportunityShare"] = modeling["Opportunities"] / modeling["Team_Total_Plays"].replace(0, pd.NA)
modeling["TPRR"] = modeling["Targets"] / modeling["Routes Run"].replace(0, pd.NA)
modeling["YPRR"] = modeling["Air Yards"] / modeling["Routes Run"].replace(0, pd.NA)
modeling["AirYardsShare"] = modeling["Air Yards"] / modeling.groupby(["Year", "Team"])["Air Yards"].transform("sum")

modeling["RedZoneShare"] = modeling["Red Zone Touches"] / modeling.groupby(["Year", "Team"])["Red Zone Touches"].transform("sum")
modeling["GoalLineShare"] = modeling["Goal Line Touches"] / modeling.groupby(["Year", "Team"])["Goal Line Touches"].transform("sum")

# === Save final enriched dataset ===
output_path = os.path.join(base_dir, "modeling_final_enriched.csv")
modeling.to_csv(output_path, index=False)

print(f"Enriched modeling dataset saved to {output_path}")