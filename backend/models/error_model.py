#backend/models/error_model.py
import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from features import build_temperature_features


# ==================================================
# 1. Load data
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)
df["time"] = pd.to_datetime(df["time"])


# ==================================================
# 2. Build ORIGINAL temperature features
# ==================================================

X_full = build_temperature_features(df)

# Remove rolling-skill features.
# We only want the original features for this experiment.

original_columns = [
    "hour",
    "month",
    "day_of_year",
    "ifs_temp",
    "gfs_temp",
    "aifs_temp",
    "hgefs_temp",
    "temp_mean",
    "temp_std",
    "temp_min",
    "temp_max",
]

X = X_full[original_columns]


# ==================================================
# 3. Models we want to predict error for
# ==================================================

models = {
    "IFS": "ifs_temp",
    "GFS": "gfs_temp",
    "AIFS": "aifs_temp",
    "HGEFS": "hgefs_temp",
}


# ==================================================
# 4. Chronological split
# ==================================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]


# ==================================================
# 5. XGBoost settings
# ==================================================

params = {
    "n_estimators": 300,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "random_state": 42,
}


# ==================================================
# 6. Train one error model per weather model
# ==================================================

results = {}

for model_name, forecast_column in models.items():

    print(f"\nTraining error model for {model_name}...")

    # Actual historical absolute error
    y = (
        df[forecast_column] - df["era5_temp"]
    ).abs()

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # Train XGBoost
    model = XGBRegressor(**params)

    model.fit(
        X_train,
        y_train
    )

    # Predict error on unseen test period
    predictions = model.predict(X_test)

    # ------------------------------
    # XGBoost performance
    # ------------------------------

    xgb_mae = mean_absolute_error(
        y_test,
        predictions
    )

    xgb_rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    # ------------------------------
    # Baseline performance
    # ------------------------------

    baseline_value = y_train.mean()

    baseline_predictions = [
        baseline_value
    ] * len(y_test)

    baseline_mae = mean_absolute_error(
        y_test,
        baseline_predictions
    )

    baseline_rmse = mean_squared_error(
        y_test,
        baseline_predictions
    ) ** 0.5

    # ------------------------------
    # Improvement
    # ------------------------------

    mae_improvement = (
        (baseline_mae - xgb_mae)
        / baseline_mae
    ) * 100

    rmse_improvement = (
        (baseline_rmse - xgb_rmse)
        / baseline_rmse
    ) * 100

    results[model_name] = {
        "baseline_mae": baseline_mae,
        "xgb_mae": xgb_mae,
        "baseline_rmse": baseline_rmse,
        "xgb_rmse": xgb_rmse,
        "mae_improvement": mae_improvement,
        "rmse_improvement": rmse_improvement,
    }


# ==================================================
# 7. Print results
# ==================================================

print("\n")
print("=" * 65)
print("TEMPERATURE ERROR PREDICTION — ALL MODELS")
print("=" * 65)

print(
    f"{'Model':<10}"
    f"{'Base MAE':>12}"
    f"{'XGB MAE':>12}"
    f"{'Improvement':>15}"
)

print("-" * 65)

for model_name, result in results.items():

    print(
        f"{model_name:<10}"
        f"{result['baseline_mae']:>12.3f}"
        f"{result['xgb_mae']:>12.3f}"
        f"{result['mae_improvement']:>14.2f}%"
    )

print("\n")

print(
    f"{'Model':<10}"
    f"{'Base RMSE':>12}"
    f"{'XGB RMSE':>12}"
    f"{'Improvement':>15}"
)

print("-" * 65)

for model_name, result in results.items():

    print(
        f"{model_name:<10}"
        f"{result['baseline_rmse']:>12.3f}"
        f"{result['xgb_rmse']:>12.3f}"
        f"{result['rmse_improvement']:>14.2f}%"
    )