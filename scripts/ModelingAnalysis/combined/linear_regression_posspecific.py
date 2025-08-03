# Use dimensionality reduction instead of dropping.

# PCA or feature selection via Random Forest/XGBoost feature importance keeps multicollinear features but reduces redundancy.

import pandas as pd
import numpy as np
import glob
import os
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

print("Current working directory:", os.getcwd())

positions = ['QB', 'RB', 'WR', 'TE']
target = 'Fantasy Points'

features_dict = {
    'QB': [
        'Passing Yards (Advanced)', 'Completions 10+ Yards', 'Pass Attempts (Advanced)',
        'Completions 20+ Yards', 'Pocket Time', 'Red Zone Attempts', 'Rushing Attempts'
    ],
    'RB': [
        'relevent_snaps_played', 'Rushing Yards (Advanced)', 'Yards Before Contact',
        'redzone_touches', 'Receptions (Advanced)', 'goal_line_touches', 'Tackles for Loss',
        'Broken Tackles', 'Yards After Contact (Advanced)', 'Runs 10+ Yards'
    ],
    'WR': [
        'Receptions (Advanced)', 'receiving_yards', 'Receptions 10+ Yards', 'routes_run',
        'Yards After Catch', 'redzone_touches', 'Red Zone Targets'
    ],
    'TE': [
        'Receiving Yards (Advanced)', 'Receptions 10+ Yards', 'Receptions (Advanced)',
        'Targets (Advanced)', 'routes_run', 'Yards Before Catch', 'redzone_touches'
    ]
}

os.makedirs("models", exist_ok=True)

for pos in positions:
    print(f"\n--- {pos} Pipeline ---")
    folder = f'/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/{pos.lower()}'
    pattern = f'*{pos}_merged*.csv'
    file_pattern = os.path.join(folder, pattern)
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files found for {pos} in {folder}")
        continue

    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, skiprows=[1])
            df.columns = df.columns.str.strip().str.replace('"', '')
            dfs.append(df)
        except Exception as e:
            print(f"Could not read {f}: {e}")
    if not dfs:
        print(f"No data loaded for {pos}")
        continue

    pos_df = pd.concat(dfs, ignore_index=True)

    features = [f for f in features_dict[pos] if f in pos_df.columns]
    if not features:
        print(f"No features found for {pos}")
        continue

    # Clean numeric columns
    for col in features:
        pos_df[col] = pd.to_numeric(pos_df[col].astype(str).str.replace(',', ''), errors='coerce')
    if target in pos_df.columns:
        pos_df[target] = pd.to_numeric(pos_df[target].astype(str).str.replace(',', ''), errors='coerce')
    else:
        print(f"Target '{target}' not found for {pos}")
        continue

    # Drop rows with all-NaN features
    pos_df = pos_df.dropna(subset=features, how='all')
    X = pos_df[features]
    y = pos_df[target]

    # Impute and scale
    imputer = SimpleImputer(strategy='mean')
    scaler = StandardScaler()
    X = pd.DataFrame(imputer.fit_transform(X), columns=features)
    X_scaled = scaler.fit_transform(X)
    y = y.fillna(y.mean())

    # PCA: keep enough components to explain 95% of variance
    pca = PCA(n_components=0.95, svd_solver='full')
    X_pca = pca.fit_transform(X_scaled)
    print(f"PCA: Reduced from {X.shape[1]} to {X_pca.shape[1]} components.")

    # Model training
    X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("R²:", r2_score(y_test, y_pred))
    print("RMSE:", rmse)

    # Cross-validation
    scores = cross_val_score(model, X_pca, y, cv=5, scoring='r2')
    print("Cross-validated R²:", scores.mean())

    # Save everything needed for inference
    joblib.dump(model, f"models/{pos}_linear_model.joblib")
    joblib.dump(imputer, f"models/{pos}_imputer.joblib")
    joblib.dump(scaler, f"models/{pos}_scaler.joblib")
    joblib.dump(pca, f"models/{pos}_pca.joblib")
    print(f"Saved model, imputer, scaler, and PCA for {pos} to models/")

# Now, in the future, you can load these with:
# model = joblib.load("models/QB_linear_model.joblib")
# imputer = joblib.load("models/QB_imputer.joblib")
# scaler = joblib.load("models/QB_scaler.joblib")
# pca = joblib.load("models/QB_pca.joblib")

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))