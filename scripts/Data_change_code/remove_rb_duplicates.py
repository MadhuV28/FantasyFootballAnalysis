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

    if 'player_id' in df.columns:
        df = df.drop_duplicates(subset='player_id', keep='first')
    elif 'Player' in df.columns:
        df = df.drop_duplicates(subset='Player', keep='first')
    else:
        df = df.drop_duplicates(keep='first')

    df.to_csv(csv_file, index=False)
    print(f"Removed duplicates from: {csv_file}")