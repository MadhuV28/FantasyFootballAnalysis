# Set number of threads for linear algebra libraries
import os
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"
import pandas as pd
import glob

# Map positions to their subfolder and file pattern
position_info = {
    'QB': {'folder': 'qb', 'pattern': '*QB_merged*.csv'},
    'RB': {'folder': 'rb', 'pattern': '*RB_merged*.csv'},
    'WR': {'folder': 'wr', 'pattern': '*WR_merged*.csv'},
    'TE': {'folder': 'te', 'pattern': '*TE_merged*.csv'},
}

target = 'Fantasy Points'  # or 'Fantasy Points/Game' or 'PPG'

output_dir = '/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/linearRegression_featureSelection'
os.makedirs(output_dir, exist_ok=True)

summary_results = []

for pos, info in position_info.items():
    print(f"\n=== Top correlated features for {pos}s (using all subfolder files) ===")
    file_pattern = os.path.join('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo', info['folder'], info['pattern'])
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files found for {pos} in {info['folder']}")
        continue
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, skiprows=[1])
            df.columns = df.columns.str.strip().str.replace('"', '')
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
    numeric_cols = pos_df.select_dtypes(include='number').columns
    if target in numeric_cols:
        corrs = pos_df[numeric_cols].corr()[target].sort_values(ascending=False)
        print(corrs.head(20))
        # Save per-position correlations
        corrs.to_csv(f'{output_dir}/{pos}_feature_correlations.csv')
        # Collect top 5 for summary
        for feature, corr in corrs.head(5).items():
            if feature != target:
                summary_results.append({
                    "Position": pos,
                    "Feature": feature,
                    "CorrelationWithTarget": corr
                })
    else:
        print(f"Target '{target}' not found in numeric columns for {pos}s.")

# Save summary of top features across positions
summary_df = pd.DataFrame(summary_results)
summary_df.to_csv(f'{output_dir}/top_feature_correlations_summary.csv', index=False)
print("\n=== Summary of top features across positions ===")