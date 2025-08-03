import pandas as pd
import os

files = {
    "rb": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years.csv",
    "wr": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/wr_all_years.csv",
    "te": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/te_all_years.csv"
}
out_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"

for pos, path in files.items():
    df = pd.read_csv(path)
    year_col = "Year"
    # Try to find the team column
    team_col = None
    for col in df.columns:
        if col.lower() == "posteam" or col.lower() == "team":
            team_col = col
            break
    if not team_col:
        print(f"Could not find team column in {pos} file. Columns are: {df.columns.tolist()}")
        continue
    if pos == "rb":
        carries_col = "Rushing Attempts (Advanced)"
        targets_col = "Targets (Advanced)"
    else:
        carries_col = None
        targets_col = "Targets (Advanced)"
    if carries_col and carries_col in df.columns:
        df["Player_Opps"] = pd.to_numeric(df[carries_col], errors="coerce").fillna(0) + pd.to_numeric(df[targets_col], errors="coerce").fillna(0)
    else:
        df["Player_Opps"] = pd.to_numeric(df[targets_col], errors="coerce").fillna(0)
    team_totals = df.groupby([year_col, team_col])["Player_Opps"].sum().reset_index().rename(columns={"Player_Opps": "Team_Opps"})
    merged = df.merge(team_totals, on=[year_col, team_col], how="left")
    merged["opportunity_share"] = merged["Player_Opps"] / merged["Team_Opps"]
    merged.to_csv(os.path.join(out_dir, f"{pos}_all_years_with_opp_share.csv"), index=False)
    print(f"Wrote {pos}_all_years_with_opp_share.csv")