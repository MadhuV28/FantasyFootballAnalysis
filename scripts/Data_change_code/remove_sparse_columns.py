import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
    df = pd.read_csv(csv_file, low_memory=False)
    # Count empty or NaN entries per column
    mask = df.isnull() | (df.astype(str).apply(lambda x: x.str.strip() == ""))
    cols_to_drop = mask.sum() >= 20
    df = df.loc[:, ~cols_to_drop]
    df.to_csv(csv_file, index=False)
    print(f"Removed sparse columns from {csv_file}")