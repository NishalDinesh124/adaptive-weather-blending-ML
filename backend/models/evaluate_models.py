#backend/models/evaluate_models.py
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training_dataset.csv"


df = pd.read_csv(DATA_FILE)


models = {
    "IFS": ("ifs_temp", "ifs_precip"),
    "GFS": ("gfs_temp", "gfs_precip"),
    "AIFS": ("aifs_temp", "aifs_precip"),
    "HGEFS": ("hgefs_temp", "hgefs_precip"),
}


print("\n===== TEMPERATURE PERFORMANCE =====")

for name, (temp_col, _) in models.items():
    mae = mean_absolute_error(df["era5_temp"], df[temp_col])
    rmse = mean_squared_error(df["era5_temp"], df[temp_col]) ** 0.5

    print(f"{name:6} | MAE: {mae:.3f} °C | RMSE: {rmse:.3f} °C")


print("\n===== PRECIPITATION PERFORMANCE =====")

for name, (_, precip_col) in models.items():
    mae = mean_absolute_error(df["era5_precip"], df[precip_col])
    rmse = mean_squared_error(df["era5_precip"], df[precip_col]) ** 0.5

    print(f"{name:6} | MAE: {mae:.3f} mm | RMSE: {rmse:.3f} mm")