import pandas as pd

df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')
df[df.columns[21]] = pd.to_numeric(df[df.columns[21]].str.replace(',', ''), errors='coerce').astype('Int64')
df[df.columns[23]] = pd.to_numeric(df[df.columns[23]].str.replace(',', ''), errors='coerce').astype('Int64')