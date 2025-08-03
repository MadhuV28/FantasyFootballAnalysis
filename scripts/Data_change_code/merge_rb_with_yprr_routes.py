import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"
yprr_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/other/yprr_metrics/yprr_metrics_2015.csv"
routes_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/other/routes_metrics/routes_metrics_2015.csv"

# Load metrics, keep only columns (not index) and player_name_std
yprr_df = pd.read_csv(yprr_path)
routes_df = pd.read_csv(routes_path)

# Remove duplicate columns if any
metrics_df = yprr_df.merge(routes_df, on="player_name_std", how="outer", suffixes=('_yprr', '_routes'))

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    rb_df = pd.read_csv(csv_file)
    # Merge on player_name_std, only add columns from metrics_df
    merged_df = rb_df.merge(metrics_df, on="player_name_std", how="left")
    merged_df.to_csv(csv_file, index=False)
    print(f"Merged metrics into {csv_file}")