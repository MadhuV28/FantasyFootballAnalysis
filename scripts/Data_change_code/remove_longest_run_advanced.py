import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue
    if "Longest Run (Advanced)" in df.columns:
        df = df.drop(columns=["Longest Run (Advanced)"])
        print(f"Removed 'Longest Run (Advanced)' from: {csv_file}")
    df.to_csv(csv_file, index=False)