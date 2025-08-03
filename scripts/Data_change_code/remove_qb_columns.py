import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

cols_to_remove = [
    "player_name_std", "player_name", "attempts", "completions",
    "receiver_player_id_yac_metrics_2020", "receiver_player_name_yac_metrics_2020",
    "receiver_player_id_yac_metrics_2018", "receiver_player_name_yac_metrics_2018",
    "player_id_redzone_metrics_2024", "player_name_redzone_metrics_2024",
    "player_id_redzone_metrics_2023", "player_name_redzone_metrics_2023",
    "player_id_redzone_metrics_2022", "player_name_redzone_metrics_2022",
    "player_id_redzone_metrics_2020", "player_name_redzone_metrics_2020",
    "player_id_redzone_metrics_2019", "player_name_redzone_metrics_2019",
    "player_id_redzone_metrics_2018", "player_name_redzone_metrics_2018",
    "player_id_redzone_metrics_2017", "player_name_redzone_metrics_2017",
    "player_id_redzone_metrics_2016", "player_name_redzone_metrics_2016",
    "player_id_redzone_metrics_2015", "player_name_redzone_metrics_2015",
    "sacks"
]

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Removed columns from {csv_file}")