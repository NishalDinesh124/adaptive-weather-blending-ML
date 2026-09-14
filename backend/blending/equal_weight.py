#backend/blending/equal_weight.py
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)


# Equal weights
WEIGHTS = {
    "ifs": 0.25,
    "gfs": 0.25,
    "aifs": 0.25,
    "hgefs": 0.25,
}


# --------------------------------------------------
# Temperature blend
# --------------------------------------------------

df["blend_temp"] = (
    WEIGHTS["ifs"] * df["ifs_temp"]
    + WEIGHTS["gfs"] * df["gfs_temp"]
    + WEIGHTS["aifs"] * df["aifs_temp"]
    + WEIGHTS["hgefs"] * df["hgefs_temp"]
)


# --------------------------------------------------
# Precipitation blend
# --------------------------------------------------

df["blend_precip"] = (
    WEIGHTS["ifs"] * df["ifs_precip"]
    + WEIGHTS["gfs"] * df["gfs_precip"]
    + WEIGHTS["aifs"] * df["aifs_precip"]
    + WEIGHTS["hgefs"] * df["hgefs_precip"]
)


# --------------------------------------------------
# Evaluate temperature
# --------------------------------------------------

temp_mae = mean_absolute_error(
    df["era5_temp"],
    df["blend_temp"]
)

temp_rmse = mean_squared_error(
    df["era5_temp"],
    df["blend_temp"]
) ** 0.5


# --------------------------------------------------
# Evaluate precipitation
# --------------------------------------------------

precip_mae = mean_absolute_error(
    df["era5_precip"],
    df["blend_precip"]
)

precip_rmse = mean_squared_error(
    df["era5_precip"],
    df["blend_precip"]
) ** 0.5


# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n===== EQUAL-WEIGHT BLEND =====")

print("\nWeights:")
for model, weight in WEIGHTS.items():
    print(f"{model.upper():6} → {weight * 100:.0f}%")

print("\nTemperature:")
print(f"MAE  : {temp_mae:.3f} °C")
print(f"RMSE : {temp_rmse:.3f} °C")

print("\nPrecipitation:")
print(f"MAE  : {precip_mae:.3f} mm")
print(f"RMSE : {precip_rmse:.3f} mm")