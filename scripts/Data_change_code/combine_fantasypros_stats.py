import pandas as pd
import re

input_path = "/Users/mvuyyuru/Downloads/FantasyPros_Fantasy_Football_Leaders_2025.csv"
output_path = "/Users/mvuyyuru/Downloads/FantasyPros_Fantasy_Football_Leaders_2025_combined.csv"

# Read the raw CSV as lines
with open(input_path, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

stat_tables = []
current_stat = None
current_rows = []

for line in lines:
    # Detect a new stat table by header
    if line.startswith('"Player"') and ',' in line:
        if current_stat and current_rows:
            df = pd.DataFrame(current_rows, columns=current_stat)
            stat_tables.append(df)
            current_rows = []
        # Parse header
        current_stat = [col.strip('"') for col in line.split(",")]
    elif line.startswith('"') and ',' in line:
        # Data row
        row = [col.strip('"') for col in line.split(",")]
        if len(row) == len(current_stat):
            current_rows.append(row)

# Add the last table
if current_stat and current_rows:
    df = pd.DataFrame(current_rows, columns=current_stat)
    stat_tables.append(df)

# Merge all tables on Player and Team
from functools import reduce

# Clean up column names to be unique
for df in stat_tables:
    for col in df.columns:
        if col not in ["Player", "Team"]:
            # Rename stat column to be unique if needed
            if col in ["Player", "Team"]:
                continue
            if col in df.columns[df.columns.duplicated()].tolist():
                df.rename(columns={col: col + "_dup"}, inplace=True)

# Merge all tables
def merge_tables(left, right):
    return pd.merge(left, right, on=["Player", "Team"], how="outer")

merged = reduce(merge_tables, stat_tables)

# Remove duplicate columns if any
merged = merged.loc[:, ~merged.columns.duplicated()]

# Save to CSV
merged.to_csv(output_path, index=False)
print(f"Combined CSV saved to: {output_path}")