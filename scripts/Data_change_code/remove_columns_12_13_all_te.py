import os
import pandas as pd
import glob

te_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/te"

for csv_file in glob.glob(os.path.join(te_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue

    # Only drop if there are enough columns
    if df.shape[1] > 12:
        df = df.drop(df.columns[[11, 12]], axis=1)
        df.to_csv(csv_file, index=False)
        print(f"Removed columns 12 and 13 from: {csv_file}")
    else:
        print(f"Skipped (not enough columns): {csv_file}")