import os
import pandas as pd
import glob

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo"
out_dir = os.path.join(base_dir, "pos_combined_year")
os.makedirs(out_dir, exist_ok=True)

positions = {
    "qb": "qb_all_years.csv",
    "rb": "rb_all_years.csv",
    "wr": "wr_all_years.csv",
    "te": "te_all_years.csv"
}

for pos, out_file in positions.items():
    pos_dir = os.path.join(base_dir, pos)
    all_dfs = []
    for csv_file in glob.glob(os.path.join(pos_dir, "*.csv")):
        try:
            df = pd.read_csv(csv_file)
        except Exception:
            continue
        # Add 'Year' column if not present, try to infer from filename
        if 'Year' not in df.columns:
            basename = os.path.basename(csv_file)
            year = None
            for part in basename.split("_"):
                if part[:4].isdigit():
                    year = int(part[:4])
                    break
            if year:
                df['Year'] = year
        all_dfs.append(df)
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.to_csv(os.path.join(out_dir, out_file), index=False)
        print(f"Created {out_file} in {out_dir}")
    else:
        print(f"No data found for {pos}")