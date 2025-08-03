import os
import pandas as pd
import glob

qb_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/qb"

descriptions = [
    "The player’s overall fantasy Ranking",
    "The quarterback’s name (display format).",
    "Season fantasy points scored.",
    "Average fantasy points scored per game.",
    "Number of passing touchdowns.",
    "Number of interceptions.",
    "Total passing yards (may include advanced adjustments or air yards components).",
    "Percentage of passes completed (advanced stat — may adjust for drops, throwaways, etc.).",
    "Average passing yards per attempt (advanced calculation).",
    "Completion Percentage Over Expected (accuracy relative to expected completions based on throw difficulty).",
    "Total completed passes (advanced version, may adjust for specific situations).",
    "Total pass attempts (advanced version).",
    "Total distance (in yards) that all pass attempts traveled in the air (before catch).",
    "Average air yards per pass attempt.",
    "Number of completed passes that gained 10 or more yards.",
    "Number of completed passes that gained 20 or more yards.",
    "Number of completed passes that gained 30 or more yards.",
    "Number of completed passes that gained 40 or more yards.",
    "Number of completed passes that gained 50 or more yards.",
    "Number of pass attempts made inside the opponent’s 20-yard line.",
    "Quarterback rating (passer efficiency metric using completions, yards, TDs, INTs).",
    "Average time (in seconds) the QB spends in the pocket before releasing the ball or being pressured/sacked.",
    "Total number of times the QB was sacked (advanced tracking).",
    "Ratio of pressures that resulted in a sack (measures QB’s ability to avoid sacks when pressured).",
    "Number of times the QB was hit or knocked down (but not necessarily sacked).",
    "Number of times the QB was hurried (forced to throw earlier than intended).",
    "Number of defensive blitzes the QB faced.",
    "Number of passes classified as poorly thrown (off-target).",
    "Number of passes dropped by receivers.",
    "Total rushing touchdowns scored by the QB.",
    "Total rushing yards gained by the QB.",
    "Total rushing attempts by the QB.",
    "Number of fumbles lost (turnovers).",
    "Number of games played (advanced tracking; may account for partial appearances).",
    "Unique player identifier (database reference).",
    "Season year for the stats.",
    "Number of times the QB was pressured by defenders (includes hits, hurries, sacks)."
]

for csv_file in glob.glob(os.path.join(qb_dir, "*.csv")):
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