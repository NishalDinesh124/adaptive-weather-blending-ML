# backend/blending/adaptive_blend.py
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR=Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR/"backend" / "models"))

from features import build_temperature_features


# ============================================================
# 1. LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)
df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time").reset_index(drop=True)


# ============================================================
# 2. BUILD FEATURES
# ============================================================

X_full = build_temperature_features(df)

feature_columns = [
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

X = X_full[feature_columns]


# ============================================================
# 3. MODELS
# ============================================================

forecast_models = {
    "IFS": "ifs_temp",
    "GFS": "gfs_temp",
    "AIFS": "aifs_temp",
    "HGEFS": "hgefs_temp",
}


params = {
    "n_estimators": 300,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "random_state": 42,
}


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

test_df = df.iloc[split_index:].copy()


# ============================================================
# 5. TRAIN FOUR ERROR MODELS
# ============================================================

predicted_errors = {}

for model_name, forecast_column in forecast_models.items():

    print(f"Training error model: {model_name}")

    # Target = actual absolute forecast error
    y = (
        df[forecast_column]
        - df["era5_temp"]
    ).abs()

    y_train = y.iloc[:split_index]

    model = XGBRegressor(**params)

    model.fit(
        X_train,
        y_train
    )

    predicted_errors[model_name] = model.predict(X_test)


# ============================================================
# 6. CREATE PREDICTED-ERROR DATAFRAME
# ============================================================

error_predictions = pd.DataFrame(
    predicted_errors,
    index=test_df.index
)

print("\nPredicted errors:")
print(error_predictions.head())


# ============================================================
# 7. CONVERT ERRORS → RELIABILITY SCORES
# ============================================================

EPSILON = 1e-6

scores = 1 / (
    error_predictions + EPSILON
)


# ============================================================
# 8. NORMALIZE SCORES → WEIGHTS
# ============================================================

weights = scores.div(
    scores.sum(axis=1),
    axis=0
)

print("\nDynamic weights:")
print(weights.head())


# ============================================================
# 9. CREATE HYBRID TEMPERATURE FORECAST
# ============================================================

test_df["hybrid_temp"] = 0.0

for model_name, forecast_column in forecast_models.items():

    test_df["hybrid_temp"] += (
        weights[model_name]
        * test_df[forecast_column]
    )


# ============================================================
# 10. EVALUATE HYBRID
# ============================================================

hybrid_mae = mean_absolute_error(
    test_df["era5_temp"],
    test_df["hybrid_temp"]
)

hybrid_rmse = mean_squared_error(
    test_df["era5_temp"],
    test_df["hybrid_temp"]
) ** 0.5


# ============================================================
# 11. EVALUATE INDIVIDUAL MODELS
# ============================================================

print("\n")
print("=" * 65)
print("TEMPERATURE FORECAST PERFORMANCE")
print("=" * 65)

for model_name, forecast_column in forecast_models.items():

    mae = mean_absolute_error(
        test_df["era5_temp"],
        test_df[forecast_column]
    )

    rmse = mean_squared_error(
        test_df["era5_temp"],
        test_df[forecast_column]
    ) ** 0.5

    print(
        f"{model_name:<10}"
        f" MAE: {mae:.3f}"
        f" | RMSE: {rmse:.3f}"
    )


# ============================================================
# 12. EQUAL-WEIGHT BASELINE
# ============================================================

test_df["equal_blend_temp"] = (
    0.25 * test_df["ifs_temp"]
    + 0.25 * test_df["gfs_temp"]
    + 0.25 * test_df["aifs_temp"]
    + 0.25 * test_df["hgefs_temp"]
)

equal_mae = mean_absolute_error(
    test_df["era5_temp"],
    test_df["equal_blend_temp"]
)

equal_rmse = mean_squared_error(
    test_df["era5_temp"],
    test_df["equal_blend_temp"]
) ** 0.5


# ============================================================
# 13. FINAL COMPARISON
# ============================================================

print("\n")
print("=" * 65)
print("BLENDING COMPARISON")
print("=" * 65)

print(
    f"Equal Blend     | "
    f"MAE: {equal_mae:.3f} "
    f"| RMSE: {equal_rmse:.3f}"
)

print(
    f"Adaptive XGB    | "
    f"MAE: {hybrid_mae:.3f} "
    f"| RMSE: {hybrid_rmse:.3f}"
)


# ============================================================
# 14. CHECK WEIGHTS
# ============================================================

print("\n")
print("=" * 65)
print("WEIGHT CHECK")
print("=" * 65)

print(weights.head(10))

print("\nWeight sums:")
print(weights.sum(axis=1).head())