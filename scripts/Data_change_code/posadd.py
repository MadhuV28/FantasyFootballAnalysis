import pandas as pd
import re

# Load your files
modeling_df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/modeling_final.csv')
proj_df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted.csv')

# Clean player names: remove " (TEAM)" from modeling_final and projections
def clean_name(name):
    return re.sub(r'\s*\(.*?\)', '', str(name)).strip()

modeling_df['PLAYER_CLEAN'] = modeling_df['Player'].apply(clean_name)
proj_df['PLAYER_CLEAN'] = proj_df['PLAYER'].apply(clean_name)

# Extract base position (e.g., "RB" from "RB5")
modeling_df['BASE_POS'] = modeling_df['Position'].astype(str).str.extract(r'([A-Z]+)')

# Build a lookup: cleaned player name -> base position
pos_lookup = dict(zip(modeling_df['PLAYER_CLEAN'], modeling_df['BASE_POS']))

# Map position to projections file using cleaned player name
proj_df['POS'] = proj_df['PLAYER_CLEAN'].map(pos_lookup)

# Save the result (drop helper column if you want)
proj_df.drop(columns=['PLAYER_CLEAN'], inplace=True)
proj_df.to_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted_with_pos.csv', index=False)
print("Added POS column and saved to: /Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted_with_pos.csv")