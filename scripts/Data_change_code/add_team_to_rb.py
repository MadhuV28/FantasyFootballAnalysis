import pandas as pd
import re

rb_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years.csv"
out_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/rb_all_years_with_team.csv"

df = pd.read_csv(rb_path)

def extract_team(player):
    m = re.search(r'\((\w+)\)', str(player))
    return m.group(1) if m else ""

df["posteam"] = df["Player"].apply(extract_team)
df.to_csv(out_path, index=False)
print(f"Wrote {out_path}")