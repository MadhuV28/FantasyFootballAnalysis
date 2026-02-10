import pandas as pd
import os

def load_player_pool(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "data", "2025_adp_VORP_draft.csv")
    df = pd.read_csv(csv_path)
    # Clean up columns if needed (e.g., fillna, strip whitespace, etc.)
    df = df.dropna(subset=["Player", "POS"])
    # Remove Joe Mixon from the player pool (case-insensitive)
    df = df[df['Player'].str.strip().str.lower() != 'joe mixon']
    return df

if __name__ == "__main__":
    pool = load_player_pool()
    print(pool.head())