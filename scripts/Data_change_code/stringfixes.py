import pandas as pd

csv_path = '/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted_with_pos.csv'
df = pd.read_csv(csv_path)

# Convert column 14 and 5 (zero-indexed: 13 and 4) to numeric
df.iloc[:, 13] = pd.to_numeric(df.iloc[:, 13], errors='coerce')
df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')

# Save back to CSV
df.to_csv(csv_path, index=False)
print("Columns 14 and 5 converted to numeric.")