import os
import glob

wr_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/wr"

descriptions = [
    "Overall fantasy ranking for the player",
    "Player name",
    "Total fantasy points scored",
    "Average fantasy points per game",
    "Receptions (advanced tracking)",
    "Targets (advanced tracking)",
    "Target share percentage",
    "Catchable targets",
    "Number of drops",
    "Receiving yards (advanced tracking)",
    "Yards per reception (advanced)",
    "Air yards",
    "Air yards per reception",
    "Yards before catch",
    "Yards before catch per reception",
    "Yards after catch (YAC)",
    "Yards after catch per reception",
    "Yards after contact",
    "Yards after contact per reception",
    "Broken tackles",
    "Receiving touchdowns (basic)",
    "Receptions of 10+ yards",
    "Receptions of 20+ yards",
    "Receptions of 30+ yards",
    "Receptions of 40+ yards",
    "Receptions of 50+ yards",
    "Longest reception (advanced)",
    "Red zone targets",
    "Routes run",
    "Yards per route run (YPRR)",
    "Targets per route run (TPRR)",
    "Rushing attempts",
    "Rushing yards",
    "Rushing touchdowns",
    "Fumbles lost",
    "Red zone touches",
    "Goal line touches",
    "Games played (advanced tracking)",
    "Rostered percentage",
    "Season year",
    "Player position",
    "Posteam",
    "Unique player identifier",
    "Player display name",
    "Games played (basic)",
    "Player name (standardized)",
    "Receiver player ID",
    "Receiver player name",
    "Receiving yards (raw)",
    "Targets (raw)",
    "Yards after catch (raw)"
]

for csv_file in glob.glob(os.path.join(wr_dir, "*.csv")):
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