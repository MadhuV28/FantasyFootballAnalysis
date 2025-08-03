import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
from sklearn.impute import SimpleImputer

df = pd.read_csv('DataInfo/pos_combined_year/modeling_final_enriched.csv')

positions = ['QB', 'RB', 'WR', 'TE']
target = 'Fantasy Points'  # or 'PPG' if you prefer

# You can manually select features for each position based on your correlation analysis
features_dict = {
    'QB': ['Attempts', 'Completions', 'Passing Yards', 'Passing TD', 'Interceptions', 'Rushing Yards', 'Rushing TD'],
    'RB': ['Carries', 'Rushing Yards', 'Rushing TD', 'Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'RedZoneShare'],
    'WR': ['Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'TPRR', 'YPRR', 'RedZoneShare'],
    'TE': ['Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'TPRR', 'YPRR', 'RedZoneShare']
}

imputer = SimpleImputer(strategy='mean')

for pos in positions:
    print(f"\n--- {pos} Linear Regression ---")
    pos_df = df[df['Position'] == pos].copy()
    features = [f for f in features_dict[pos] if f in pos_df.columns]
    # Remove features that are all-NaN
    features = [f for f in features if not pos_df[f].isna().all()]
    min_non_nan = int(0.3 * len(pos_df))
    features = [f for f in features if pos_df[f].notna().sum() >= min_non_nan]
    if not features:
        print(f"All features are empty for {pos}")
        continue
    # Clean numeric columns: remove commas and convert to float
    for col in features:
        pos_df[col] = pos_df[col].astype(str).str.replace(',', '').replace('', 'nan').astype(float)
    # Remove duplicate player-season rows if any
    if 'player_id' in pos_df.columns and 'Year' in pos_df.columns:
        pos_df = pos_df.drop_duplicates(subset=['player_id', 'Year'])
    X = pos_df[features]
    y = pos_df[target]
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=features)
    y = y.fillna(y.mean())
    print(f"Initial rows for {pos}: {len(df[df['Position'] == pos])}")
    print(f"Rows after dropping all-NaN features: {len(pos_df)}")
    print(f"Rows after deduplication: {len(X)}")
    print("Non-NaN counts per feature:")
    print(pos_df[features].notna().sum())
    if len(X) < 5:
        print("Not enough data for", pos)
        continue

    # Feature engineering example for RBs
    if pos == 'RB' and all(f in X.columns for f in ['Carries', 'Receptions']):
        X['Carries_x_Receptions'] = X['Carries'] * X['Receptions']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("Features used:", list(X.columns))
    print("R²:", r2_score(y_test, y_pred))
    print("RMSE:", rmse)

    if len(features) == 0 or len(pos_df[features].dropna()) < 10:
        # fallback: use top 3 features with most data
        feature_counts = pos_df.notna().sum().sort_values(ascending=False)
        features = [f for f in feature_counts.index if f in features_dict[pos]][:3]
        print(f"Fallback features for {pos}: {features}")

rb_df = df[df['Position'] == 'RB']
# Now, after you see the output, update the next line with the correct column name:
rb_stats = rb_df[['Player', 'Year', 'Games Played', 'Fantasy Points', 'Carries', 'Rushing Yards', 'Rushing TD', 'Receptions', 'receiving_yards', 'Receiving TD (Basic)']]