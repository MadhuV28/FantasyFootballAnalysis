import pandas as pd

input_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED.csv"
output_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025proj/FantasyPros_Fantasy_Football_Projections_2025_ALL_COMBINED_sorted.csv"

# Read the CSV
df = pd.read_csv(input_path)

# Convert FPTS to numeric, handle commas and errors
df['FPTS'] = pd.to_numeric(df['FPTS'].astype(str).str.replace(',', ''), errors='coerce')

# Remove rows where FPTS is missing or not a number
df = df.dropna(subset=['FPTS'])

# Sort by FPTS descending
df_sorted = df.sort_values('FPTS', ascending=False)

# Save to new CSV
df_sorted.to_csv(output_path, index=False)
print(f"Sorted CSV saved to: {output_path}")