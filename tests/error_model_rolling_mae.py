# tests/error_model_rolling_mae.py
import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from features import build_temperature_features


# ============================================================
# 1. LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)
df["time"] = pd.to_datetime(df["time"])

# Make absolutely sure data is chronological
df = df.sort_values("time").reset_index(drop=True)


# ============================================================
# 2. BUILD FEATURES
# ============================================================

X_full = build_temperature_features(df)


# Features WITHOUT rolling historical skill
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

X_basic = X_full[original_columns]


# Features WITH rolling historical skill
rolling_columns = [
    column
    for column in X_full.columns
    if column not in original_columns
]

X_rolling = X_full[original_columns + rolling_columns]


# ============================================================
# 3. MODELS
# ============================================================

models = {
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
# 4. REMOVE ROWS WHERE ROLLING FEATURES ARE NOT AVAILABLE
# ============================================================

valid_rows = X_rolling.notna().all(axis=1)

df_valid = df.loc[valid_rows].reset_index(drop=True)
X_basic_valid = X_basic.loc[valid_rows].reset_index(drop=True)
X_rolling_valid = X_rolling.loc[valid_rows].reset_index(drop=True)


# ============================================================
# 5. CHRONOLOGICAL TRAIN / TEST SPLIT
# ============================================================

split_index = int(len(df_valid) * 0.8)

X_basic_train = X_basic_valid.iloc[:split_index]
X_basic_test = X_basic_valid.iloc[split_index:]

X_rolling_train = X_rolling_valid.iloc[:split_index]
X_rolling_test = X_rolling_valid.iloc[split_index:]


# ============================================================
# 6. TRAIN ALL 8 MODELS
# ============================================================

results = {}


for model_name, forecast_column in models.items():

    print("\n" + "=" * 65)
    print(f"TRAINING {model_name}")
    print("=" * 65)

    # --------------------------------------------------------
    # TARGET = ABSOLUTE FORECAST ERROR
    # --------------------------------------------------------

    y = (
        df_valid[forecast_column]
        - df_valid["era5_temp"]
    ).abs()

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]


    # ========================================================
    # BASIC MODEL
    # ========================================================

    print(f"\n{model_name} — WITHOUT rolling skill")

    basic_model = XGBRegressor(**params)

    basic_model.fit(
        X_basic_train,
        y_train
    )

    basic_predictions = basic_model.predict(
        X_basic_test
    )

    basic_mae = mean_absolute_error(
        y_test,
        basic_predictions
    )

    basic_rmse = mean_squared_error(
        y_test,
        basic_predictions
    ) ** 0.5


    # ========================================================
    # ROLLING-SKILL MODEL
    # ========================================================

    print(f"{model_name} — WITH rolling skill")

    rolling_model = XGBRegressor(**params)

    rolling_model.fit(
        X_rolling_train,
        y_train
    )

    rolling_predictions = rolling_model.predict(
        X_rolling_test
    )

    rolling_mae = mean_absolute_error(
        y_test,
        rolling_predictions
    )

    rolling_rmse = mean_squared_error(
        y_test,
        rolling_predictions
    ) ** 0.5


    # ========================================================
    # STORE RESULTS
    # ========================================================

    results[model_name] = {
        "basic_mae": basic_mae,
        "basic_rmse": basic_rmse,
        "rolling_mae": rolling_mae,
        "rolling_rmse": rolling_rmse,
    }


# ============================================================
# 7. PRINT RESULTS
# ============================================================

print("\n\n")
print("=" * 85)
print("ROLLING SKILL FEATURE EXPERIMENT")
print("=" * 85)

print(
    f"{'Model':<10}"
    f"{'Basic MAE':>12}"
    f"{'Rolling MAE':>14}"
    f"{'MAE Δ':>12}"
    f"{'Basic RMSE':>14}"
    f"{'Rolling RMSE':>16}"
    f"{'RMSE Δ':>12}"
)

print("-" * 85)


for model_name, result in results.items():

    mae_difference = (
        result["rolling_mae"]
        - result["basic_mae"]
    )

    rmse_difference = (
        result["rolling_rmse"]
        - result["basic_rmse"]
    )

    print(
        f"{model_name:<10}"
        f"{result['basic_mae']:>12.3f}"
        f"{result['rolling_mae']:>14.3f}"
        f"{mae_difference:>+12.3f}"
        f"{result['basic_rmse']:>14.3f}"
        f"{result['rolling_rmse']:>16.3f}"
        f"{rmse_difference:>+12.3f}"
    )


# ============================================================
# 8. INTERPRETATION
# ============================================================

print("\n")
print("Interpretation:")
print("  Negative Δ  = rolling skill IMPROVED performance")
print("  Positive Δ  = rolling skill WORSENED performance")
print("  Δ is Rolling - Basic")