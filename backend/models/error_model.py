import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from features import build_temperature_features


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)
df["time"] = pd.to_datetime(df["time"])


# --------------------------------------------------
# 2. Build features
# --------------------------------------------------

X = build_temperature_features(df)

# Actual IFS temperature error
y = (df["ifs_temp"] - df["era5_temp"]).abs()


# --------------------------------------------------
# 3. Chronological train/test split
# --------------------------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


# --------------------------------------------------
# 4. XGBoost error model
# --------------------------------------------------

model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
)

model.fit(X_train, y_train)

xgb_pred = model.predict(X_test)


# --------------------------------------------------
# 5. Dumb baseline
# --------------------------------------------------

# Predict the same error for every test sample:
# the mean error observed during training.

baseline_prediction = y_train.mean()

baseline_pred = [baseline_prediction] * len(y_test)


# --------------------------------------------------
# 6. Evaluate both
# --------------------------------------------------

xgb_mae = mean_absolute_error(y_test, xgb_pred)
xgb_rmse = mean_squared_error(y_test, xgb_pred) ** 0.5

baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_rmse = mean_squared_error(y_test, baseline_pred) ** 0.5


# --------------------------------------------------
# 7. Results
# --------------------------------------------------

print("\n===== IFS TEMPERATURE ERROR PREDICTION =====")

print(f"Training rows : {len(X_train)}")
print(f"Testing rows  : {len(X_test)}")

print("\n--- Baseline ---")
print(f"MAE  : {baseline_mae:.3f} °C")
print(f"RMSE : {baseline_rmse:.3f} °C")

print("\n--- XGBoost ---")
print(f"MAE  : {xgb_mae:.3f} °C")
print(f"RMSE : {xgb_rmse:.3f} °C")

print("\n--- Improvement ---")

mae_improvement = (
    (baseline_mae - xgb_mae) / baseline_mae
) * 100

rmse_improvement = (
    (baseline_rmse - xgb_rmse) / baseline_rmse
) * 100

print(f"MAE improvement  : {mae_improvement:.2f}%")
print(f"RMSE improvement : {rmse_improvement:.2f}%")


# --------------------------------------------------
# 8. Inspect predictions
# --------------------------------------------------

print("\n--- First 10 predictions ---")

for actual, predicted in zip(
    y_test.iloc[:10],
    xgb_pred[:10]
):
    print(
        f"Actual error: {actual:.3f} °C | "
        f"Predicted: {predicted:.3f} °C"
    )