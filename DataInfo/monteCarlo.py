import numpy as np
import pandas as pd

def simulate_player_points(mean, std, n_sim=1000, min_floor=0):
    """
    Simulate fantasy points for a player using a normal distribution.
    Returns an array of simulated points.
    """
    sims = np.random.normal(loc=mean, scale=std, size=n_sim)
    sims = np.maximum(sims, min_floor)  # No negative points
    return sims

def simulate_team(df, mean_col='ProjMean', std_col='ProjStd', n_sim=1000):
    """
    Simulate fantasy points for all players in a DataFrame.
    Returns a DataFrame with simulation results for each player.
    """
    results = {}
    for idx, row in df.iterrows():
        sims = simulate_player_points(row[mean_col], row[std_col], n_sim)
        results[row['Player']] = sims
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
    # Example player projections
    data = [
        {'Player': 'Player A', 'ProjMean': 15, 'ProjStd': 4},
        {'Player': 'Player B', 'ProjMean': 10, 'ProjStd': 3},
        {'Player': 'Player C', 'ProjMean': 8, 'ProjStd': 2},
    ]
    df_proj = pd.DataFrame(data)
    sims = simulate_team(df_proj)
    summary = summarize_simulation(sims)
    print(summary)