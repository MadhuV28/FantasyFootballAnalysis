import pandas as pd
import glob
import os

# Mapping of position folders to relevant metrics folders in DataInfo/other
position_map = {
    "qb": ["qb_metrics"],
    "rb": ["yac_metrics", "redzone_metrics"],
    "wr": ["yprr_metrics", "routes_metrics", "redzone_metrics", "yac_metrics"],
    "te": ["yprr_metrics", "routes_metrics", "redzone_metrics", "yac_metrics"]
}

# Helper to get year from filename (assumes format ...YEAR.csv)
def get_year_from_filename(filename):
    basename = os.path.basename(filename)
    for part in basename.split("_"):
        if part[:4].isdigit():
            return part[:4]
    # fallback: try last 8 chars (e.g. 2015WR.csv)
    for part in basename.split(".")[0].split("R")[-1].split("Q")[-1].split("T")[-1].split("E")[-1]:
        if part.isdigit() and len(part) == 4:
            return part
    return None

# Merge function for one position and one year
def merge_position_metrics(pos, pos_file, metrics_map):
    year = get_year_from_filename(pos_file)
    pos_df = pd.read_csv(pos_file)
    merged = pos_df.copy()
    for metric_folder in metrics_map:
        metric_files = glob.glob(f"DataInfo/other/{metric_folder}/*{year}*.csv")
        for metric_file in metric_files:
            metric_df = pd.read_csv(metric_file)
            # Find season/year column in metric_df
            season_col = None
            for col in metric_df.columns:
                if col.lower() in ["season", "year"]:
                    season_col = col
                    break
            if not season_col:
                continue
            # Drop columns from metric_df that already exist in merged (except join keys)
            join_keys = ["player_name_std", season_col]
            metric_df = metric_df[[col for col in metric_df.columns if col not in merged.columns or col in join_keys]]
            merged = pd.merge(
                merged,
                metric_df,
                left_on=["player_name_std", "Year"],
                right_on=["player_name_std", season_col],
                how="left",
                suffixes=('', f'_{metric_folder}')
            )
            # Optionally, drop duplicate season/year columns after merge
            if season_col in merged.columns and "Year" in merged.columns and season_col != "Year":
                merged = merged.drop(columns=[season_col])
    return merged

# Loop through all positions and years
for pos, metrics in position_map.items():
    pos_files = glob.glob(f"DataInfo/{pos}/*.csv")
    for pos_file in pos_files:
        merged_df = merge_position_metrics(pos, pos_file, metrics)
        year = get_year_from_filename(pos_file)
        outname = f"DataInfo/{pos}/{year}{pos.upper()}_merged.csv"
        merged_df.to_csv(outname, index=False)
        print(f"Merged {pos_file} with metrics for year {year} -> {outname}")