import os
import pandas as pd
import glob

wr_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/wr"

for csv_file in glob.glob(os.path.join(wr_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue
    # Only drop if there are enough columns
    drop_indices = [11, 12, 31, 33, 34]
    drop_indices = [i for i in drop_indices if i < df.shape[1]]
    df = df.drop(df.columns[drop_indices], axis=1)
    df.to_csv(csv_file, index=False)
    print(f"Removed columns 12, 13, 32, 34, 35 from: {csv_file}")