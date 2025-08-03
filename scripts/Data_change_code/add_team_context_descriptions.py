import os
import glob

team_context_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/team_context"

descriptions = [
    "Season year",
    "Team abbreviation",
    "Average number of offensive plays run per game",
    "Neutral situation pass rate (fraction of plays that are passes in neutral game script)"
]

for csv_file in glob.glob(os.path.join(team_context_dir, "*.csv")):
    with open(csv_file, "r") as f:
        lines = f.readlines()
    # Only add if not already present
    if len(lines) > 1 and descriptions[0] in lines[1]:
        print(f"Descriptions already present in: {csv_file}")
        continue
    header = lines[0].strip().split(",")
    desc_row = descriptions[:len(header)] + [""] * (len(header) - len(descriptions))
    desc_line = ",".join(f'"{d}"' for d in desc_row) + "\n"
    new_lines = [lines[0], desc_line] + lines[1:]
    with open(csv_file, "w") as f:
        f.writelines(new_lines)
    print(f"Added descriptions to: {csv_file}")