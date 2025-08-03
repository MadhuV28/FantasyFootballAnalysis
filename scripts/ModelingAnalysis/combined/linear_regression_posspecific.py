# Use dimensionality reduction instead of dropping.
import os
import csv

# PCA or feature selection via Random Forest/XGBoost feature importance keeps multicollinear features but reduces redundancy.
# Set number of threads for linear algebra libraries
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"

import pandas as pd
import numpy as np
import glob
import os
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

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

results = []

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
    r2 = r2_score(y_test, y_pred)
    print("R²:", r2)
    print("RMSE:", rmse)

    # Cross-validation
    scores = cross_val_score(model, X_pca, y, cv=5, scoring='r2')
    cv_r2 = scores.mean()
    print("Cross-validated R²:", cv_r2)

    # --- Random Forest ---
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=2)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_r2 = r2_score(y_test, rf_pred)
    rf_cv_r2 = cross_val_score(rf_model, X_pca, y, cv=5, scoring='r2', n_jobs=1).mean()
    print(f"Random Forest: R²={rf_r2:.4f}, RMSE={rf_rmse:.4f}, Cross-validated R²={rf_cv_r2:.4f}")

    # --- XGBoost ---
    xgb_model = XGBRegressor(n_estimators=100, random_state=42, n_jobs=2, verbosity=0)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    xgb_r2 = r2_score(y_test, xgb_pred)
    xgb_cv_r2 = cross_val_score(xgb_model, X_pca, y, cv=5, scoring='r2', n_jobs=1).mean()
    print(f"XGBoost: R²={xgb_r2:.4f}, RMSE={xgb_rmse:.4f}, Cross-validated R²={xgb_cv_r2:.4f}")

    # --- Random Forest with GridSearchCV ---
    rf_param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 5, 10]
    }
    rf_gs = GridSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=2),
        rf_param_grid,
        cv=3,
        scoring='r2',
        n_jobs=1
    )
    rf_gs.fit(X_train, y_train)
    rf_best = rf_gs.best_estimator_
    rf_pred = rf_best.predict(X_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_r2 = r2_score(y_test, rf_pred)
    rf_cv_r2 = cross_val_score(rf_best, X_pca, y, cv=5, scoring='r2', n_jobs=1).mean()
    print(f"Random Forest (best): R²={rf_r2:.4f}, RMSE={rf_rmse:.4f}, Cross-validated R²={rf_cv_r2:.4f}, Best Params: {rf_gs.best_params_}")

    # Save Random Forest model
    joblib.dump(rf_best, f"models/{pos}_randomforest_model.joblib")

    # --- XGBoost with GridSearchCV ---
    xgb_param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [3, 5, 7]
    }
    xgb_gs = GridSearchCV(
        XGBRegressor(random_state=42, n_jobs=2, verbosity=0),
        xgb_param_grid,
        cv=3,
        scoring='r2',
        n_jobs=1
    )
    xgb_gs.fit(X_train, y_train)
    xgb_best = xgb_gs.best_estimator_
    xgb_pred = xgb_best.predict(X_test)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    xgb_r2 = r2_score(y_test, xgb_pred)
    xgb_cv_r2 = cross_val_score(xgb_best, X_pca, y, cv=5, scoring='r2', n_jobs=1).mean()
    print(f"XGBoost (best): R²={xgb_r2:.4f}, RMSE={xgb_rmse:.4f}, Cross-validated R²={xgb_cv_r2:.4f}, Best Params: {xgb_gs.best_params_}")

    # Save XGBoost model
    joblib.dump(xgb_best, f"models/{pos}_xgboost_model.joblib")

    # Save all results for this position
    results.append({
        "Position": pos,
        "Model": "LinearRegression",
        "Num_Original_Features": X.shape[1],
        "Num_PCA_Components": X_pca.shape[1],
        "R2": r2,
        "RMSE": rmse,
        "CV_R2": cv_r2
    })
    results.append({
        "Position": pos,
        "Model": "RandomForest",
        "Num_Original_Features": X.shape[1],
        "Num_PCA_Components": X_pca.shape[1],
        "R2": rf_r2,
        "RMSE": rf_rmse,
        "CV_R2": rf_cv_r2,
        "Best_Params": str(rf_gs.best_params_)
    })
    results.append({
        "Position": pos,
        "Model": "XGBoost",
        "Num_Original_Features": X.shape[1],
        "Num_PCA_Components": X_pca.shape[1],
        "R2": xgb_r2,
        "RMSE": xgb_rmse,
        "CV_R2": xgb_cv_r2,
        "Best_Params": str(xgb_gs.best_params_)
    })

# --- Save results to a new CSV for all models ---
output_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/linearRegression"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, "all_models_posspecific_results.csv")

with open(output_csv, "w", newline="") as csvfile:
    fieldnames = [
        "Position", "Model", "Num_Original_Features", "Num_PCA_Components",
        "R2", "RMSE", "CV_R2", "Best_Params"  # <-- add Best_Params here
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\nSaved all model results to {output_csv}")

# Now, in the future, you can load these with:
# model = joblib.load("models/QB_linear_model.joblib")
# imputer = joblib.load("models/QB_imputer.joblib")
# scaler = joblib.load("models/QB_scaler.joblib")
# pca = joblib.load("models/QB_pca.joblib")

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))