import os
import pandas as pd

metrics = [
    "qb_metrics",
    "receiving",
    "redzone_metrics",
    "routes_metrics",
    "team_context",
    "yac_metrics",
    "yprr_metrics"
]

base_dir = "DataInfo/other"

for metric in metrics:
    input_csv = os.path.join(base_dir, f"{metric}.csv")
    output_dir = os.path.join(base_dir, metric)
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    year_col = "season" if "season" in df.columns else "year"
    for year in df[year_col].unique():
        df_year = df[df[year_col] == year]
        out_path = os.path.join(output_dir, f"{metric}_{year}.csv")
        df_year.to_csv(out_path, index=False)
        print(f"Saved {out_path}")