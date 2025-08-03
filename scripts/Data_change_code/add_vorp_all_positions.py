import pandas as pd
import os

files = {
    "rb": {
        "path": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years.csv",
        "out": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_vorp.csv",
        "replacement_rank": 24  # RB24
    },
    "wr": {
        "path": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/wr_all_years.csv",
        "out": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/wr_all_years_with_vorp.csv",
        "replacement_rank": 36  # WR36
    },
    "te": {
        "path": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/te_all_years.csv",
        "out": "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/te_all_years_with_vorp.csv",
        "replacement_rank": 12  # TE12
    }
}

for pos, info in files.items():
    df = pd.read_csv(info["path"])
    for year in df["Year"].unique():
        year_df = df[df["Year"] == year]
        replacement = year_df["Fantasy Points"].sort_values(ascending=False).reset_index(drop=True)
        if len(replacement) >= info["replacement_rank"]:
            rep_val = replacement.iloc[info["replacement_rank"] - 1]
        else:
            rep_val = replacement.iloc[-1]
        df.loc[df["Year"] == year, "VORP"] = pd.to_numeric(df.loc[df["Year"] == year, "Fantasy Points"], errors="coerce") - rep_val
    df.to_csv(info["out"], index=False)
    print(f"Wrote {info['out']}")

df['vorp_description'] = 'Value Over Replacement Player'
df.to_csv('yourfile_with_description.csv', index=False)