import pandas as pd
import os

rb_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_opp_share.csv"
team_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/team_context/team_context_2024.csv"
out_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_opp_snap_share.csv"

df = pd.read_csv(rb_path)
team = pd.read_csv(team_path)
team.columns = [c.strip().lower() for c in team.columns]
team = team.rename(columns={"season": "Year", "posteam": "posteam", "plays_per_game": "plays_per_game"})

# Only for 2024, but you can expand for all years if you have team context for all years
df_2024 = df[df["Year"] == 2024].copy()
df_2024 = df_2024.merge(team[["Year", "posteam", "plays_per_game"]], left_on=["Year", "posteam"], right_on=["Year", "posteam"], how="left")
df_2024["snap_share"] = pd.to_numeric(df_2024["relevent_snaps_played"], errors="coerce") / pd.to_numeric(df_2024["plays_per_game"], errors="coerce")
df_2024.to_csv(out_path, index=False)
print(f"Wrote {out_path}")

carries_col = "carries" in df_2024.columns
targets_col = "targets" in df_2024.columns
team_col = "posteam" in df_2024.columns
year_col = "Year" in df_2024.columns

if not (carries_col and targets_col and team_col and year_col):
    pass