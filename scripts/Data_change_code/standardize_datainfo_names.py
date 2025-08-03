import os
import pandas as pd

DATAINFO_PATH = "."
POSITIONS = ["qb", "rb", "wr", "te"]
OTHER_PATH = os.path.join(DATAINFO_PATH, "other")

def standardize_player_name(full_name):
    # Remove team info if present
    name = str(full_name).split('(')[0].strip()
    parts = name.split()
    if len(parts) < 2:
        return None
    first, last = parts[0], parts[-1]
    return f"{first[0]}.{last}"

def process_csv(path):
    df = pd.read_csv(path)
    # Find any column containing 'player_name'
    player_name_cols = [col for col in df.columns if 'player_name' in col]
    if 'Player' in df.columns:
        df['player_name_std'] = df['Player'].apply(standardize_player_name)
        df.to_csv(path, index=False)
        print(f"Updated {path} (from 'Player')")
    elif player_name_cols:
        # Use the first matching column
        df['player_name_std'] = df[player_name_cols[0]]
        df.to_csv(path, index=False)
        print(f"Updated {path} (from '{player_name_cols[0]}')")
    else:
        print(f"Skipped {path} (no 'Player' or '*player_name*' column)")

def get_all_players():
    players = set()
    for pos in POSITIONS:
        pos_path = os.path.join(DATAINFO_PATH, pos)
        for fname in os.listdir(pos_path):
            if fname.endswith(".csv"):
                df = pd.read_csv(os.path.join(pos_path, fname))
                # Try to find standardized name column
                std_col = [c for c in df.columns if "player_name_std" in c]
                if std_col:
                    players.update(df[std_col[0]].astype(str).str.strip())
    return players

def filter_other_files(players):
    for root, _, files in os.walk(OTHER_PATH):
        for fname in files:
            if fname.endswith(".csv"):
                fpath = os.path.join(root, fname)
                df = pd.read_csv(fpath)
                std_col = [c for c in df.columns if "player_name_std" in c]
                if std_col:
                    df = df[df[std_col[0]].astype(str).str.strip().isin(players)]
                    df.to_csv(fpath, index=False)

base_dir = "DataInfo"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".csv"):
            path = os.path.join(root, file)
            try:
                process_csv(path)
            except Exception as e:
                print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    all_players = get_all_players()
    filter_other_files(all_players)