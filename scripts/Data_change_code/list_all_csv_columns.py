import os
import pandas as pd
import glob

base = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo"
folders = ["pos_combined_year", "qb", "rb", "te", "team_context", "wr"]

for folder in folders:
    folder_path = os.path.join(base, folder)
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue
    csvs = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csvs:
        print(f"No CSVs found in {folder_path}")
        continue
    print(f"\n=== Folder: {folder} ===")
    for csv in csvs:
        try:
            df = pd.read_csv(csv, nrows=0)
            print(f"\nFile: {os.path.basename(csv)}")
            print(f"Columns: {list(df.columns)}")
        except Exception as e:
            print(f"Could not read {csv}: {e}")

# Also include modeling_final.csv if it exists
modeling_final_path = os.path.join(base, "modeling_final.csv")
if os.path.exists(modeling_final_path):
    try:
        df = pd.read_csv(modeling_final_path, nrows=0)
        print(f"\n=== File: modeling_final.csv ===")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Could not read modeling_final.csv: {e}")

# Also include modeling_final_enriched.csv if it exists
modeling_final_enriched_path = os.path.join(base, "modeling_final_enriched.csv")
if os.path.exists(modeling_final_enriched_path):
    try:
        df = pd.read_csv(modeling_final_enriched_path, nrows=0)
        print(f"\n=== File: modeling_final_enriched.csv ===")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Could not read modeling_final_enriched.csv: {e}")