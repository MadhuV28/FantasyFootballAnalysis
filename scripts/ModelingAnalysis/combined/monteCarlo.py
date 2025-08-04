import pandas as pd
import numpy as np

# Load your combined projections file
csv_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted_with_pos.csv"
df = pd.read_csv(csv_path)

# Clean FPTS column (remove commas, convert to float)
df['FPTS'] = pd.to_numeric(df['FPTS'].astype(str).str.replace(',', ''), errors='coerce')

# Drop rows without FPTS or PLAYER
df = df.dropna(subset=['PLAYER', 'FPTS'])

# Assign standard deviation by position
std_map = {
    'RB': 7.6,
    'WR': 7.2,
    'TE': 6.4,
    'QB': 7.4
}
# If your file uses a different column for position, adjust 'POS' below
df['FPTS_STD'] = df['POS'].map(std_map).fillna(5.0)  # Default to 5.0 if position missing

def simulate_player_points(mean, std, n_sim=1000, min_floor=0):
    """
    Simulate fantasy points for a player using a normal distribution.
    Returns an array of simulated points.
    """
    sims = np.random.normal(loc=mean, scale=std, size=n_sim)
    sims = np.maximum(sims, min_floor)  # No negative points
    return sims

def simulate_team(df, mean_col='FPTS', std_col='FPTS_STD', n_sim=1000):
    """
    Simulate fantasy points for all players in a DataFrame.
    Returns a DataFrame with simulation results for each player.
    """
    results = {}
    for idx, row in df.iterrows():
        sims = simulate_player_points(row[mean_col], row[std_col], n_sim)
        results[row['PLAYER']] = sims
    return pd.DataFrame(results)

def summarize_simulation(sims):
    """
    Given a DataFrame of simulations (players as columns), return summary stats.
    """
    summary = {}
    for player in sims.columns:
        vals = sims[player]
        summary[player] = {
            'floor': np.percentile(vals, 10),
            'median': np.percentile(vals, 50),
            'ceiling': np.percentile(vals, 90),
            'mean': np.mean(vals),
            'std': np.std(vals)
        }
    return pd.DataFrame(summary).T

# Example usage:
if __name__ == "__main__":
    # Use real data for simulation
    sims = simulate_team(df, mean_col='FPTS', std_col='FPTS_STD', n_sim=1000)
    summary = summarize_simulation(sims)
    # Save summary to CSV
    output_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/monte_carlo_fpts_summary.csv"
    summary.to_csv(output_path)
    print(f"Monte Carlo summary saved to: {output_path}")
    print(summary.head())