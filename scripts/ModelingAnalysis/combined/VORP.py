import pandas as pd

# Load your projections (replace with your actual file)
projections = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/your_projection_file.csv')

# Set replacement level rank for each position (example: 12 teams, 2 RB/WR/TE starters each)
replacement_rank = {'QB': 13, 'RB': 25, 'WR': 25, 'TE': 13}

vorp_list = []

for pos in ['QB', 'RB', 'WR', 'TE']:
    pos_df = projections[projections['Position'] == pos].copy()
    pos_df = pos_df.sort_values('Projected_Fantasy_Points', ascending=False).reset_index(drop=True)
    rep_points = pos_df.iloc[replacement_rank[pos] - 1]['Projected_Fantasy_Points']
    pos_df['VORP'] = pos_df['Projected_Fantasy_Points'] - rep_points
    vorp_list.append(pos_df)

vorp_df = pd.concat(vorp_list)
vorp_df.to_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/vorp_results.csv', index=False)
print("Saved VORP results to DataInfo/vorp_results.csv")