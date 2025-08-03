import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

cols_to_remove = [
    "season_yac_metrics_2020", "yac_yac_metrics_2020",
    "season_yac_metrics_2018", "yac_yac_metrics_2018",
    "season_redzone_metrics_2024", "redzone_touches_redzone_metrics_2024", "goal_line_touches_redzone_metrics_2024",
    "season_redzone_metrics_2023", "redzone_touches_redzone_metrics_2023", "goal_line_touches_redzone_metrics_2023",
    "season_redzone_metrics_2022", "redzone_touches_redzone_metrics_2022", "goal_line_touches_redzone_metrics_2022",
    "season_redzone_metrics_2021", "redzone_touches", "goal_line_touches",
    "season_redzone_metrics_2020", "redzone_touches_redzone_metrics_2020", "goal_line_touches_redzone_metrics_2020",
    "season_redzone_metrics_2019", "redzone_touches_redzone_metrics_2019", "goal_line_touches_redzone_metrics_2019",
    "season_redzone_metrics_2018", "redzone_touches_redzone_metrics_2018", "goal_line_touches_redzone_metrics_2018",
    "season_redzone_metrics_2017", "redzone_touches_redzone_metrics_2017", "goal_line_touches_redzone_metrics_2017",
    "season_redzone_metrics_2016", "redzone_touches_redzone_metrics_2016", "goal_line_touches_redzone_metrics_2016",
    "season_redzone_metrics_2015", "redzone_touches_redzone_metrics_2015", "goal_line_touches_redzone_metrics_2015"
]

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Removed specified columns from {csv_file}")