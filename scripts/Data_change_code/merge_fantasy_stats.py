import pandas as pd
import os
import re

# QB column mapping for descriptive names
QB_COL_MAP = {
    "Rank": "Rank",
    "Player": "Player",
    "CMP": "Completions",
    "ATT_x": "Pass Attempts (Basic)",
    "PCT_x": "Completion % (Basic)",
    "YDS_x": "Passing Yards (Basic)",
    "Y/A_x": "Yards/Attempt (Basic)",
    "TD": "Passing TD",
    "INT": "Interceptions",
    "SACKS": "Sacks (Basic)",
    "ATT.1": "Rushing Attempts",
    "YDS.1": "Rushing Yards",
    "TD.1": "Rushing TD",
    "FL": "Fumbles Lost",
    "G_x": "Games Played (Basic)",
    "FPTS": "Fantasy Points",
    "FPTS/G": "Fantasy Points/Game",
    "ROST": "Rostered %",
    "G_y": "Games Played (Advanced)",
    "COMP": "Completions (Advanced)",
    "ATT_y": "Pass Attempts (Advanced)",
    "PCT_y": "Completion % (Advanced)",
    "YDS_y": "Passing Yards (Advanced)",
    "Y/A_y": "Yards/Attempt (Advanced)",
    "AIR": "Air Yards",
    "AIR/A": "Air Yards/Attempt",
    "10+ YDS": "Completions 10+ Yards",
    "20+ YDS": "Completions 20+ Yards",
    "30+ YDS": "Completions 30+ Yards",
    "40+ YDS": "Completions 40+ Yards",
    "50+ YDS": "Completions 50+ Yards",
    "PKT TIME": "Pocket Time",
    "SACK": "Sacks (Advanced)",
    "KNCK": "QB Hits/Knockdowns",
    "HRRY": "QB Hurries",
    "BLITZ": "Blitzes Faced",
    "POOR": "Poor Throws",
    "DROP": "Receiver Drops",
    "RZ ATT": "Red Zone Attempts",
    "RTG": "QB Rating",
    "Year": "Year",
    "Position": "Position"
}

# RB column mapping for descriptive names
RB_COL_MAP = {
    "Rank": "Rank",
    "Player": "Player",
    "ATT_x": "Rushing Attempts (Basic)",
    "YDS_x": "Rushing Yards (Basic)",
    "Y/A": "Yards/Attempt (Basic)",
    "LG": "Longest Run",
    "20+": "Runs 20+ Yards",
    "TD": "Rushing TD (Basic)",
    "REC_x": "Receptions (Basic)",
    "TGT_x": "Targets (Basic)",
    "YDS.1": "Receiving Yards (Basic)",
    "Y/R": "Yards/Reception (Basic)",
    "TD.1": "Receiving TD (Basic)",
    "FL": "Fumbles Lost",
    "G_x": "Games Played (Basic)",
    "FPTS": "Fantasy Points",
    "FPTS/G": "Fantasy Points/Game",
    "ROST": "Rostered %",
    "G_y": "Games Played (Advanced)",
    "ATT_y": "Rushing Attempts (Advanced)",
    "YDS_y": "Rushing Yards (Advanced)",
    "Y/ATT": "Yards/Attempt (Advanced)",
    "YBCON": "Yards Before Contact",
    "YBCON/ATT": "Yards Before Contact/Attempt",
    "YACON": "Yards After Contact",
    "YACON/ATT": "Yards After Contact/Attempt",
    "BRKTKL": "Broken Tackles",
    "TK LOSS": "Tackles for Loss",
    "TK LOSS YDS": "Tackles for Loss Yards",
    "LNG TD": "Longest TD Run",
    "10+ YDS": "Runs 10+ Yards",
    "20+ YDS": "Runs 20+ Yards (Advanced)",
    "30+ YDS": "Runs 30+ Yards",
    "40+ YDS": "Runs 40+ Yards",
    "50+ YDS": "Runs 50+ Yards",
    "LNG": "Longest Run (Advanced)",
    "REC_y": "Receptions (Advanced)",
    "TGT_y": "Targets (Advanced)",
    "RZ TGT": "Red Zone Targets",
    "YACON.1": "Yards After Contact (Advanced)",
    "Year": "Year",
    "Position": "Position"
}

# WR column mapping for descriptive names
WR_COL_MAP = {
    "Rank": "Rank",
    "Player": "Player",
    "REC_x": "Receptions (Basic)",
    "TGT_x": "Targets (Basic)",
    "YDS_x": "Receiving Yards (Basic)",
    "Y/R_x": "Yards/Reception (Basic)",
    "LG": "Longest Reception",
    "20+": "Receptions 20+ Yards",
    "TD": "Receiving TD (Basic)",
    "ATT": "Rushing Attempts",
    "YDS.1": "Rushing Yards",
    "TD.1": "Rushing TD",
    "FL": "Fumbles Lost",
    "G_x": "Games Played (Basic)",
    "FPTS": "Fantasy Points",
    "FPTS/G": "Fantasy Points/Game",
    "ROST": "Rostered %",
    "G_y": "Games Played (Advanced)",
    "REC_y": "Receptions (Advanced)",
    "YDS_y": "Receiving Yards (Advanced)",
    "Y/R_y": "Yards/Reception (Advanced)",
    "YBC": "Yards Before Catch",
    "YBC/R": "Yards Before Catch/Reception",
    "AIR": "Air Yards",
    "AIR/R": "Air Yards/Reception",
    "YAC": "Yards After Catch",
    "YAC/R": "Yards After Catch/Reception",
    "YACON": "Yards After Contact",
    "YACON/R": "Yards After Contact/Reception",
    "BRKTKL": "Broken Tackles",
    "TGT_y": "Targets (Advanced)",
    "% TM": "Target Share %",
    "CATCHABLE": "Catchable Targets",
    "DROP": "Drops",
    "RZ TGT": "Red Zone Targets",
    "10+ YDS": "Receptions 10+ Yards",
    "20+ YDS": "Receptions 20+ Yards",
    "30+ YDS": "Receptions 30+ Yards",
    "40+ YDS": "Receptions 40+ Yards",
    "50+ YDS": "Receptions 50+ Yards",
    "LNG": "Longest Reception (Advanced)",
    "Year": "Year",
    "Position": "Position"
}

# TE column mapping for descriptive names
TE_COL_MAP = {
    "Rank": "Rank",
    "Player": "Player",
    "REC_x": "Receptions (Basic)",
    "TGT_x": "Targets (Basic)",
    "YDS_x": "Receiving Yards (Basic)",
    "Y/R_x": "Yards/Reception (Basic)",
    "LG": "Longest Reception",
    "20+": "Receptions 20+ Yards",
    "TD": "Receiving TD (Basic)",
    "ATT": "Rushing Attempts",
    "YDS.1": "Rushing Yards",
    "TD.1": "Rushing TD",
    "FL": "Fumbles Lost",
    "G_x": "Games Played (Basic)",
    "FPTS": "Fantasy Points",
    "FPTS/G": "Fantasy Points/Game",
    "ROST": "Rostered %",
    "G_y": "Games Played (Advanced)",
    "REC_y": "Receptions (Advanced)",
    "YDS_y": "Receiving Yards (Advanced)",
    "Y/R_y": "Yards/Reception (Advanced)",
    "YBC": "Yards Before Catch",
    "YBC/R": "Yards Before Catch/Reception",
    "AIR": "Air Yards",
    "AIR/R": "Air Yards/Reception",
    "YAC": "Yards After Catch",
    "YAC/R": "Yards After Catch/Reception",
    "YACON": "Yards After Contact",
    "YACON/R": "Yards After Contact/Reception",
    "BRKTKL": "Broken Tackles",
    "TGT_y": "Targets (Advanced)",
    "% TM": "Target Share %",
    "CATCHABLE": "Catchable Targets",
    "DROP": "Drops",
    "RZ TGT": "Red Zone Targets",
    "10+ YDS": "Receptions 10+ Yards",
    "20+ YDS": "Receptions 20+ Yards",
    "30+ YDS": "Receptions 30+ Yards",
    "40+ YDS": "Receptions 40+ Yards",
    "50+ YDS": "Receptions 50+ Yards",
    "LNG": "Longest Reception (Advanced)",
    "Year": "Year",
    "Position": "Position"
}

def load_stats(year, position, base_path, top_n):
    files = os.listdir(base_path)
    basic_file = next((f for f in files if re.search(fr"Statistics_{position}{year}\.csv$", f)), None)
    adv_file = next((f for f in files if re.search(fr"Advanced_Stats_Report_{position}{year}\.csv$", f)), None)
    if not basic_file:
        print(f"Skipping {position}{year}: basic files not found.")
        return pd.DataFrame()
    if not adv_file:
        print(f"Skipping {position}{year}: advanced files not found.")
        return pd.DataFrame()
    basic_df = pd.read_csv(os.path.join(base_path, basic_file))
    adv_df = pd.read_csv(os.path.join(base_path, adv_file))
    merged = pd.merge(
        basic_df,
        adv_df[[c for c in adv_df.columns if c != 'Rank' or c == 'Player']],
        on="Player",
        how="left"
    )
    merged['Year'] = year
    merged['Position'] = position
    points_col = next((c for c in merged.columns if 'FPTS' in c or 'Fantasy Points' in c), None)
    if points_col:
        merged = merged.nlargest(top_n, points_col)
    # Rename columns for each position
    if position == "QB":
        merged.rename(columns={k: v for k, v in QB_COL_MAP.items() if k in merged.columns}, inplace=True)
    elif position == "RB":
        merged.rename(columns={k: v for k, v in RB_COL_MAP.items() if k in merged.columns}, inplace=True)
    elif position == "WR":
        merged.rename(columns={k: v for k, v in WR_COL_MAP.items() if k in merged.columns}, inplace=True)
    elif position == "TE":
        merged.rename(columns={k: v for k, v in TE_COL_MAP.items() if k in merged.columns}, inplace=True)
    return merged

def merge_all_stats(base_path, positions, years):
    all_stats = []
    for year in years:
        for position in positions:
            stats = load_stats(year, position, base_path)
            if not stats.empty:
                all_stats.append(stats)
    if all_stats:
        return pd.concat(all_stats, ignore_index=True)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    positions = ['QB', 'RB', 'WR', 'TE']
    years = list(range(2015, 2025))
    base_path = "/Users/mvuyyuru/Downloads/fantasyfootballdata2015-2024"
    output_dir = "Data_by_year"

    for position in positions:
        pos_dir = os.path.join(output_dir, position.lower())
        os.makedirs(pos_dir, exist_ok=True)
        top_n = 25 if position in ['QB', 'TE'] else 70
        for year in years:
            df = load_stats(year, position, base_path, top_n)
            if not df.empty:
                out_path = os.path.join(pos_dir, f"{year}{position}.csv")
                df.to_csv(out_path, index=False)
                print(f"Saved {out_path}")