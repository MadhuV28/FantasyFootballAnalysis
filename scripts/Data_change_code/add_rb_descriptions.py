import os
import pandas as pd
import glob

rb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/rb"

descriptions = [
    "Overall fantasy ranking for the player",
    "Player name",
    "Total fantasy points scored",
    "Average fantasy points per game",
    "Number of fumbles lost",
    "Games played (advanced tracking)",
    "Player position",
    "Unique player identifier",
    "Season year",
    "Yards per rushing attempt (basic)",
    "Rushing touchdowns (basic)",
    "Yards per reception (basic)",
    "Receiving touchdowns (basic)",
    "Rostered percentage",
    "Rushing attempts (advanced)",
    "Rushing yards (advanced)",
    "Yards before contact",
    "Yards before contact per attempt",
    "Yards after contact",
    "Yards after contact per attempt",
    "Broken tackles",
    "Tackles for loss",
    "Tackles for loss yards",
    "Longest touchdown run",
    "Runs of 10+ yards",
    "Runs of 20+ yards (advanced)",
    "Runs of 30+ yards",
    "Runs of 40+ yards",
    "Runs of 50+ yards",
    "Receptions (advanced)",
    "Targets (advanced)",
    "Red zone targets",
    "Yards after contact (advanced)",
    "Yards after catch (YAC)",
    "Red zone touches",
    "Goal line touches",
    "Season yards per route run (YPRR)",
    "Routes run YPRR",
    "Yards per route run (YPRR)",
    "Season routes",
    "Posteam",
    "Routes run (routes)",
    "Targets per route run (TPRR)"
]

for csv_file in glob.glob(os.path.join(rb_dir, "*.csv")):
    with open(csv_file, "r") as f:
        lines = f.readlines()
    # Only add if not already present
    if len(lines) > 1 and descriptions[0] in lines[1]:
        print(f"Descriptions already present in: {csv_file}")
        continue
    header = lines[0].strip().split(",")
    # Pad/truncate descriptions to match header length
    desc_row = descriptions[:len(header)] + [""] * (len(header) - len(descriptions))
    desc_line = ",".join(f'"{d}"' for d in desc_row) + "\n"
    new_lines = [lines[0], desc_line] + lines[1:]
    with open(csv_file, "w") as f:
        f.writelines(new_lines)
    print(f"Added descriptions to: {csv_file}")