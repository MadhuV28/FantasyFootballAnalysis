import pandas as pd

csv_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_dataset.csv"
df = pd.read_csv(csv_path)

# Find the correct column name (case-insensitive)
fp_col = None
for col in df.columns:
    if col.strip().lower() == "fantasy points":
        fp_col = col
        break

if fp_col:
    df[fp_col] = pd.to_numeric(df[fp_col], errors='coerce')
    df = df.sort_values(by=fp_col, ascending=False)
    df.to_csv(csv_path, index=False)
    print("Sorted modeling_dataset.csv by Fantasy Points.")
else:
    print("Fantasy Points column not found.")