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
    # Count empty (NaN or blank string) entries per column
    empty_counts = df.isna().sum() + (df == '').sum()
    # Drop columns where empty count >= half the number of rows
    threshold = len(df) / 2
    cols_to_drop = [col for col in df.columns if empty_counts[col] >= threshold]
    df = df.drop(columns=cols_to_drop)
    df.to_csv(csv_file, index=False)
    print(f"Removed sparse columns from: {csv_file}")