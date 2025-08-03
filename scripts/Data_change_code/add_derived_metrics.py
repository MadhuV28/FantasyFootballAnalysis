import pandas as pd

# Paths
player_csv = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_dataset.csv"
team_csv = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/team_context_all_years.csv"
out_csv = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_dataset_with_metrics.csv"

# Load data
players = pd.read_csv(player_csv)
teams = pd.read_csv(team_csv)

# Merge team context into player data
players = players.merge(
    teams,
    left_on=["Team", "Year"],
    right_on=["Team", "Year"],
    how="left"
)

# Convert relevant columns to numeric
for col in [
    "Fantasy Points", "Carries", "Receptions", "Targets", "Routes Run",
    "Receiving Yards", "Red Zone Touches", "Air Yards",
    "Total_Plays", "RedZone_Plays", "Team_AirYards"
]:
    if col in players.columns:
        players[col] = pd.to_numeric(players[col], errors="coerce").fillna(0)

# Derived metrics
players["Fantasy Points Per Touch"] = players["Fantasy Points"] / (players["Carries"] + players["Receptions"]).replace(0, pd.NA)
players["Points Per Opportunity"] = players["Fantasy Points"] / (players["Carries"] + players["Targets"]).replace(0, pd.NA)
players["Opportunity Share"] = (players["Carries"] + players["Targets"]) / players["Total_Plays"].replace(0, pd.NA)
players["Red Zone Touch Share"] = players["Red Zone Touches"] / players["RedZone_Plays"].replace(0, pd.NA)
players["TPRR"] = players["Targets"] / players["Routes Run"].replace(0, pd.NA)
players["YPRR"] = players["Receiving Yards"] / players["Routes Run"].replace(0, pd.NA)
players["Air Yards Share"] = players["Air Yards"] / players["Team_AirYards"].replace(0, pd.NA)

# Save result
players.to_csv(out_csv, index=False)
print(f"Saved with derived metrics: {out_csv}")