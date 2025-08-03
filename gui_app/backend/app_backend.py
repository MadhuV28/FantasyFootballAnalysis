# import pandas as pd
# import os

# def load_data(csv_path):
#     df = pd.read_csv(csv_path)
#     # Clean and convert all percentage columns to integer (rounded)
#     for col in df.columns:
#         if '%' in col:
#             df[col] = (
#                 df[col]
#                 .astype(str)
#                 .str.rstrip('%')
#                 .replace('', 'NaN')
#                 .astype(float)
#                 .round()
#                 .astype('Int64')
#             )
#     df['Rank'] = df.groupby(['Year', 'Position'])['Fantasy Points'].rank(method='first', ascending=False)
#     df['Group'] = df['Rank'].apply(rank_group)
#     return df

# def rank_group(r):
#     if r <= 5:
#         return 'Top 5'
#     elif r <= 10:
#         return '6-10'
#     elif r <= 20:
#         return '11-20'
#     else:
#         return '21+'

# def get_feature_correlations(correlation_dir, correlation_files):
#     feature_correlations = {}
#     for pos, fname in correlation_files.items():
#         path = os.path.join(correlation_dir, fname)
#         if os.path.exists(path):
#             corr_df = pd.read_csv(path, index_col=0)
#             feature_correlations[pos] = corr_df['Fantasy Points'].to_dict()
#         else:
#             feature_correlations[pos] = {}
#     return feature_correlations

# def filter_players(df, years=None, positions=None, players=None):
#     filtered = df.copy()
#     if positions:
#         filtered = filtered[filtered['Position'].isin(positions)]
#     if years:
#         filtered = filtered[filtered['Year'].astype(str).isin(years)]
#     if players:
#         filtered = filtered[filtered['Player'].isin(players)]
#     return filtered

# def get_unique_sorted(df, col, years=None, positions=None):
#     filtered = filter_players(df, years=years, positions=positions)
#     return sorted(filtered[col].dropna().unique())