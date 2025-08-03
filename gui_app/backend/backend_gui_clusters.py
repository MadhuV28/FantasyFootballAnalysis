import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # Clean and convert all percentage columns to integer (rounded)
    for col in df.columns:
        if '%' in col:
            df[col] = (
                df[col]
                .astype(str)
                .str.rstrip('%')
                .replace('', 'NaN')
                .astype(float)
                .round()
                .astype('Int64')
            )
    df['Rank'] = df.groupby(['Year', 'Position'])['Fantasy Points'].rank(method='first', ascending=False)
    df['Group'] = df['Rank'].apply(rank_group)
    return df

def rank_group(r):
    if r <= 5:
        return 'Top 5'
    elif r <= 10:
        return '6-10'
    elif r <= 20:
        return '11-20'
    else:
        return '21+'

def filter_df(df, years=None, positions=None, players=None):
    filtered = df.copy()
    if positions:
        filtered = filtered[filtered['Position'].isin(positions)]
    if years:
        filtered = filtered[filtered['Year'].astype(str).isin(years)]
    if players:
        filtered = filtered[filtered['Player'].isin(players)]
    return filtered

def get_unique_sorted(df, col, years=None, positions=None):
    filtered = filter_df(df, years=years, positions=positions)
    # filtered, centers = run_kmeans(filtered, x, y, n_clusters)
    return sorted(filtered[col].dropna().unique())

def run_kmeans(filtered, x, y, n_clusters):
    filtered = filtered.copy()
    filtered[x] = filtered[x].astype(str).str.replace(',', '', regex=False)
    filtered[y] = filtered[y].astype(str).str.replace(',', '', regex=False)
    filtered = filtered.dropna(subset=[x, y])
    filtered[x] = pd.to_numeric(filtered[x], errors='coerce')
    filtered[y] = pd.to_numeric(filtered[y], errors='coerce')
    X = filtered[[x, y]].astype(float).to_numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    filtered['Cluster'] = clusters
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    return filtered, centers