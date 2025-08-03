import os
import pandas as pd
import glob
import re

te_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/te"

for csv_file in glob.glob(os.path.join(te_dir, "*.csv")):
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {csv_file}")
        continue

    # Remove columns with 'Longest' and 'Reception' or 'Catch' in the name
    longest_cols = [col for col in df.columns if re.search(r'Longest.*(Reception|Catch)', col, re.IGNORECASE)]
    # Remove columns with 'Rushing' in the name
    rushing_cols = [col for col in df.columns if 'Rushing' in col]
    # Remove columns with 'Rostered %' in the name
    rostered_cols = [col for col in df.columns if 'Rostered %' in col]

    cols_to_drop = set(longest_cols + rushing_cols + rostered_cols)
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')
    df.to_csv(csv_file, index=False)
    print(f"Removed longest catch/reception, rushing, and rostered % columns from: {csv_file}")