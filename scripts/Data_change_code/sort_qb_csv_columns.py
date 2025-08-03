import pandas as pd

csv_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb/2015QB_merged_cleaned.csv"

desired_order = [
    "Rank", "Player", "Fantasy Points", "Fantasy Points/Game", "Passing TD", "Interceptions",
    "Passing Yards (Advanced)", "Completion % (Advanced)", "Yards/Attempt (Advanced)", "CPOE",
    "Completions (Advanced)", "Pass Attempts (Advanced)", "Air Yards", "Air Yards/Attempt",
    "Completions 10+ Yards", "Completions 20+ Yards", "Completions 30+ Yards", "Completions 40+ Yards",
    "Completions 50+ Yards", "Red Zone Attempts", "QB Rating", "Pocket Time", "Sacks (Advanced)",
    "Pressures", "pressure_to_sack", "QB Hits/Knockdowns", "QB Hurries", "Blitzes Faced", "Poor Throws",
    "Receiver Drops", "Rushing TD", "Rushing Yards", "Rushing Attempts", "Fumbles Lost",
    "Games Played (Advanced)", "Rostered %", "Position", "player_name_std", "player_id", "player_name",
    "attempts", "completions", "Year", "season_yac_metrics_2020", "receiver_player_id_yac_metrics_2020",
    "receiver_player_name_yac_metrics_2020", "yac_yac_metrics_2020", "season_yac_metrics_2018",
    "receiver_player_id_yac_metrics_2018", "receiver_player_name_yac_metrics_2018", "yac_yac_metrics_2018",
    "season_redzone_metrics_2024", "player_id_redzone_metrics_2024", "player_name_redzone_metrics_2024",
    "redzone_touches_redzone_metrics_2024", "goal_line_touches_redzone_metrics_2024",
    "season_redzone_metrics_2023", "player_id_redzone_metrics_2023", "player_name_redzone_metrics_2023",
    "redzone_touches_redzone_metrics_2023", "goal_line_touches_redzone_metrics_2023",
    "season_redzone_metrics_2022", "player_id_redzone_metrics_2022", "player_name_redzone_metrics_2022",
    "redzone_touches_redzone_metrics_2022", "goal_line_touches_redzone_metrics_2022",
    "season_redzone_metrics_2021", "redzone_touches", "goal_line_touches", "season_redzone_metrics_2020",
    "player_id_redzone_metrics_2020", "player_name_redzone_metrics_2020", "redzone_touches_redzone_metrics_2020",
    "goal_line_touches_redzone_metrics_2020", "season_redzone_metrics_2019", "player_id_redzone_metrics_2019",
    "player_name_redzone_metrics_2019", "redzone_touches_redzone_metrics_2019", "goal_line_touches_redzone_metrics_2019",
    "season_redzone_metrics_2018", "player_id_redzone_metrics_2018", "player_name_redzone_metrics_2018",
    "redzone_touches_redzone_metrics_2018", "goal_line_touches_redzone_metrics_2018",
    "season_redzone_metrics_2017", "player_id_redzone_metrics_2017", "player_name_redzone_metrics_2017",
    "redzone_touches_redzone_metrics_2017", "goal_line_touches_redzone_metrics_2017",
    "season_redzone_metrics_2016", "player_id_redzone_metrics_2016", "player_name_redzone_metrics_2016",
    "redzone_touches_redzone_metrics_2016", "goal_line_touches_redzone_metrics_2016",
    "season_redzone_metrics_2015", "player_id_redzone_metrics_2015", "player_name_redzone_metrics_2015",
    "redzone_touches_redzone_metrics_2015", "goal_line_touches_redzone_metrics_2015"
]

df = pd.read_csv(csv_path)

# Columns in desired order, then the rest
ordered_cols = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
df = df[ordered_cols]

df.to_csv(csv_path, index=False)
print("Columns sorted and file saved.")