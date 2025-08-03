import pandas as pd

# Load fantasy & real stats
fantasy = pd.read_csv("data/fantasy_stats.csv")
real = pd.read_csv("data/real_nfl_stats.csv")

# Merge
df = fantasy.merge(real, on=["player_id", "season"], how="left")

# Filter top players
df = df.groupby(['season','position']).apply(
    lambda x: x.nlargest(69 if x['position'].iloc[0] in ['RB','WR'] else 24, 'fantasy_points')
).reset_index(drop=True)

# Save
df.to_csv("data/final_dataset.csv", index=False)
print("Final dataset saved.")
