import os
import csv
import joblib

# Set number of threads for linear algebra libraries
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')

positions = ['QB', 'RB', 'WR', 'TE']
target = 'Fantasy Points'

features_dict = {
    'QB': ['Attempts', 'Completions', 'Passing Yards', 'Passing TD', 'Interceptions', 'Rushing Yards', 'Rushing TD'],
    'RB': ['Carries', 'Rushing Yards', 'Rushing TD', 'Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'RedZoneShare'],
    'WR': ['Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'TPRR', 'YPRR', 'RedZoneShare'],
    'TE': ['Targets', 'Receptions', 'Receiving Yards', 'Receiving TD', 'TPRR', 'YPRR', 'RedZoneShare']
}

results = []

imputer = SimpleImputer(strategy='mean')

for pos in positions:
    print(f"\n--- {pos} Models ---")
    pos_df = df[df['Position'] == pos].copy()
    features = [f for f in features_dict[pos] if f in pos_df.columns]
    features = [f for f in features if not pos_df[f].isna().all()]
    min_non_nan = int(0.3 * len(pos_df))
    features = [f for f in features if pos_df[f].notna().sum() >= min_non_nan]
    if not features:
        print(f"All features are empty for {pos}")
        continue
    for col in features:
        pos_df[col] = pos_df[col].astype(str).str.replace(',', '').replace('', 'nan').astype(float)
    if 'player_id' in pos_df.columns and 'Year' in pos_df.columns:
        pos_df = pos_df.drop_duplicates(subset=['player_id', 'Year'])
    X = pos_df[features]
    y = pos_df[target]
    X = pd.DataFrame(imputer.fit_transform(X), columns=features)
    y = y.fillna(y.mean())
    if len(X) < 5:
        print("Not enough data for", pos)
        continue

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA
    pca = PCA(n_components=0.95, svd_solver='full')
    X_pca = pca.fit_transform(X_scaled)
    print(f"PCA: Reduced from {X.shape[1]} to {X_pca.shape[1]} components.")

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=2),
        "XGBoost": XGBRegressor(n_estimators=100, random_state=42, n_jobs=2, verbosity=0)
    }

    for model_name, model in models.items():
        X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        # Warn if sample size is too small for cross-validation
        if len(X_pca) < 6:
            print(f"WARNING: Not enough samples for reliable 5-fold cross-validation for {pos} - {model_name}.")
            cv_r2 = float('nan')
        else:
            cv_r2 = cross_val_score(model, X_pca, y, cv=5, scoring='r2', n_jobs=1).mean()
        print(f"{model_name}: R²={r2:.4f}, RMSE={rmse:.4f}, Cross-validated R²={cv_r2:.4f}")

        # Save models for inference
        if model_name == "RandomForest":
            joblib.dump(model, f"models/{pos}_randomforest_model.joblib")
        elif model_name == "XGBoost":
            joblib.dump(model, f"models/{pos}_xgboost_model.joblib")
        elif model_name == "LinearRegression":
            joblib.dump(model, f"models/{pos}_linear_model.joblib")

        results.append({
            "Position": pos,
            "Model": model_name,
            "Num_Original_Features": X.shape[1],
            "Num_PCA_Components": X_pca.shape[1],
            "R2": r2,
            "RMSE": rmse,
            "CV_R2": cv_r2
        })

# Save results to CSV
output_dir = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/linearRegression"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, "all_models_all_positions_results.csv")

with open(output_csv, "w", newline="") as csvfile:
    fieldnames = ["Position", "Model", "Num_Original_Features", "Num_PCA_Components", "R2", "RMSE", "CV_R2"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\nSaved all model results to {output_csv}")

rb_df = df[df['Position'] == 'RB']
# Now, after you see the output, update the next line with the correct column name:
rb_stats = rb_df[['Player', 'Year', 'Games Played', 'Fantasy Points', 'Carries', 'Rushing Yards', 'Rushing TD', 'Receptions', 'receiving_yards', 'Receiving TD (Basic)']]