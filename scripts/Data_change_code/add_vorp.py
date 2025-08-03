import pandas as pd
import os

rb_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_opp_share.csv"
out_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_opp_share_vorp.csv"

df = pd.read_csv(rb_path)
for year in df["Year"].unique():
    year_df = df[df["Year"] == year]
    # RB24 for 12-team league
    replacement = year_df["Fantasy Points"].sort_values(ascending=False).reset_index(drop=True)
    if len(replacement) >= 24:
        rep_val = replacement.iloc[23]
    else:
        rep_val = replacement.iloc[-1]
    df.loc[df["Year"] == year, "VORP"] = pd.to_numeric(df.loc[df["Year"] == year, "Fantasy Points"], errors="coerce") - rep_val
df.to_csv(out_path, index=False)
print(f"Wrote {out_path}")