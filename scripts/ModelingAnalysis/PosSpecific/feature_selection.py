import pandas as pd
import glob
import os

# Map positions to their subfolder and file pattern
position_info = {
    'QB': {'folder': 'qb', 'pattern': '*QB_merged*.csv'},
    'RB': {'folder': 'rb', 'pattern': '*RB_merged*.csv'},
    'WR': {'folder': 'wr', 'pattern': '*WR_merged*.csv'},
    'TE': {'folder': 'te', 'pattern': '*TE_merged*.csv'},
}

target = 'Fantasy Points'  # or 'Fantasy Points/Game' or 'PPG'

output_dir = 'scripts/ModelingAnalysis/PosSpecific'
os.makedirs(output_dir, exist_ok=True)

for pos, info in position_info.items():
    print(f"\n=== Top correlated features for {pos}s (using all subfolder files) ===")
    # Find all relevant files for this position
    file_pattern = os.path.join('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo', info['folder'], info['pattern'])
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files found for {pos} in {info['folder']}")
        continue
    # Concatenate all years for this position
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, skiprows=[1])  # Skip the description row
            df.columns = df.columns.str.strip().str.replace('"', '')  # Clean column names
            # Remove commas and convert to numeric where possible
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''))
                except Exception:
                    pass
            dfs.append(df)
        except Exception as e:
            print(f"Could not read {f}: {e}")
    if not dfs:
        print(f"No data loaded for {pos}")
        continue
    pos_df = pd.concat(dfs, ignore_index=True)
    # Only keep numeric columns
    numeric_cols = pos_df.select_dtypes(include='number').columns
    # Compute correlation with target
    if target in numeric_cols:
        corrs = pos_df[numeric_cols].corr()[target].sort_values(ascending=False)
        print(corrs.head(20))
        # Save to CSV for review
        corrs.to_csv(f'{output_dir}/{pos}_feature_correlations.csv')
    else:
        print(f"Target '{target}' not found in numeric columns for {pos}s.")