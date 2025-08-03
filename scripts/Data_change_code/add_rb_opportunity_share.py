import pandas as pd
import os

rb_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years.csv"
out_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_opp_share.csv"

df = pd.read_csv(rb_path)

# Calculate player opportunities
df["Player_Opps"] = pd.to_numeric(df["Rushing Attempts (Advanced)"], errors="coerce").fillna(0) + pd.to_numeric(df["Targets (Advanced)"], errors="coerce").fillna(0)

# Calculate team totals per year
team_totals = df.groupby(["Year", "posteam"])["Player_Opps"].sum().reset_index().rename(columns={"Player_Opps": "Team_Opps"})

# Merge team totals back to player data
merged = df.merge(team_totals, on=["Year", "posteam"], how="left")

# Calculate opportunity share
merged["opportunity_share"] = merged["Player_Opps"] / merged["Team_Opps"]

# Save to new file
merged.to_csv(out_path, index=False)
print(f"Wrote {out_path}")