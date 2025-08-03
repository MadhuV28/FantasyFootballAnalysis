import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
    df = pd.read_csv(csv_file, low_memory=False)

    # Remove columns with >= 75% empty values
    thresh = len(df) * 0.25
    df = df.dropna(axis=1, thresh=thresh)

    # Remove duplicate columns (keep advanced, drop basic)
    cols_to_remove = [col for col in df.columns if "(Basic)" in col]
    df = df.drop(columns=cols_to_remove, errors='ignore')

    # Save cleaned file (overwrite original)
    df.to_csv(csv_file, index=False)
    print(f"Cleaned {csv_file}")