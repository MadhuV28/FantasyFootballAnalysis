import pandas as pd
import numpy as np
import os

base_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year"
positions = {
    "rb": {
        "file": "rb_all_years.csv",
        "carries": "Rushing Attempts (Advanced)",
        "receptions": "Receptions (Advanced)",
        "targets": "Targets (Advanced)"
    },
    "wr": {
        "file": "wr_all_years.csv",
        "carries": None,  # Usually 0 for WR
        "receptions": "Receptions (Advanced)",
        "targets": "Targets (Advanced)"
    },
    "te": {
        "file": "te_all_years.csv",
        "carries": None,  # Usually 0 for TE
        "receptions": "Receptions (Advanced)",
        "targets": "Targets (Advanced)"
    }
}

for pos, info in positions.items():
    path = os.path.join(base_dir, info["file"])
    out_path = path.replace(".csv", "_version2.csv")
    df = pd.read_csv(path)
    # Clean column names
    df.columns = [c.strip() for c in df.columns]
    # Fantasy Points per Touch
    carries = pd.to_numeric(df[info["carries"]], errors="coerce").fillna(0) if info["carries"] else 0
    receptions = pd.to_numeric(df[info["receptions"]], errors="coerce").fillna(0)
    touches = carries + receptions
    df["FantasyPointsPerTouch"] = pd.to_numeric(df["Fantasy Points"], errors="coerce") / touches.replace(0, np.nan)
    # Points per Opportunity
    targets = pd.to_numeric(df[info["targets"]], errors="coerce").fillna(0)
    opportunities = carries + targets
    df["PointsPerOpportunity"] = pd.to_numeric(df["Fantasy Points"], errors="coerce") / opportunities.replace(0, np.nan)
    # Breakout Indicator: Top 25% in opps, bottom 25% in efficiency
    high_opp = opportunities >= opportunities.quantile(0.75)
    low_eff = df["PointsPerOpportunity"] <= df["PointsPerOpportunity"].quantile(0.25)
    df["BreakoutIndicator"] = (high_opp & low_eff).astype(int)
    # Save to new file
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")