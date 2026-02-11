import os
import pandas as pd

project_root = "/Users/mvuyyuru/FantasyAnalyticsProject"
output_path = os.path.join(project_root, "all_csv_column_names.txt")

csv_info = []

for root, dirs, files in os.walk(project_root):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path, nrows=0)
                columns = list(df.columns)
                csv_info.append(f"{file_path}:\n{columns}\n")
            except Exception as e:
                csv_info.append(f"{file_path}:\nERROR: {e}\n")

with open(output_path, "w") as f:
    for info in csv_info:
        f.write(info + "\n")

print(f"Column names for all CSV files written to: {output_path}")