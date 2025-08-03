import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    df = pd.read_csv(csv_file)
    # Calculate threshold for missing values
    threshold = 40
    # Drop columns with more than half missing
    df = df.dropna(axis=1, thresh=threshold)
    df.to_csv(csv_file, index=False)
    print(f"Removed sparse columns: {csv_file}")