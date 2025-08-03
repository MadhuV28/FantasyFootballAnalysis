import os
import pandas as pd

input_csv = "DataInfo/other/air_yards_metrics.csv"
output_dir = "DataInfo/other/air_yards_metrics"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(input_csv)
for year in df['season'].unique():
    df_year = df[df['season'] == year]
    out_path = os.path.join(output_dir, f"air_yards_metrics_{year}.csv")
    df_year.to_csv(out_path, index=False)
    print(f"Saved {out_path}")