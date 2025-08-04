import pandas as pd
import re

adp_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/FantasyPros_2025_Overall_ADP_Rankings_cleaned.csv"
vorp_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/VORP_no_pos.csv"
output_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/FantasyPros_2025_Overall_ADP_Rankings_with_VORP.csv"

adp = pd.read_csv(adp_path)
vorp = pd.read_csv(vorp_path)

def clean_name(name):
    # Remove anything in parentheses and strip/normalize
    name = re.sub(r'\s*\(.*?\)', '', str(name))
    return name.replace("’", "'").replace("`", "'").replace(" Jr.", "").replace(" Sr.", "").replace(".", "").replace(",", "").strip().lower()

adp['Player_clean'] = adp['Player'].apply(clean_name)
vorp['Player_clean'] = vorp['Player'].apply(clean_name)

merged = adp.merge(
    vorp[['Player_clean', 'VORP', 'VORPvsADP']],
    on='Player_clean',
    how='left'
)

merged = merged.drop(columns=['Player_clean'])
merged.to_csv(output_path, index=False)
print(f"Saved merged file with VORP and VORPvsADP columns to {output_path}")