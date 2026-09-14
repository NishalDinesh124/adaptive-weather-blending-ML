#test_predict.py
import pandas as pd

from backend.models.predict import generate_adaptive_temperature_forecast


# Load prepared historical data
df = pd.read_csv(
    "data/processed/training_dataset.csv"
)

df["time"] = pd.to_datetime(df["time"])


# Generate adaptive forecasts
result = generate_adaptive_temperature_forecast(df)


# Show the first 10 predictions
print("\n==================================================")
print("ADAPTIVE TEMPERATURE FORECAST")
print("==================================================")

print(
    result[
        [
            "time",
            "ifs_temp",
            "gfs_temp",
            "aifs_temp",
            "hgefs_temp",
            "predicted_error_ifs",
            "predicted_error_gfs",
            "predicted_error_aifs",
            "predicted_error_hgefs",
            "weight_ifs",
            "weight_gfs",
            "weight_aifs",
            "weight_hgefs",
            "hybrid_temp",
        ]
    ].head(10).to_string(index=False)
)


# Verify weights
weight_columns = [
    "weight_ifs",
    "weight_gfs",
    "weight_aifs",
    "weight_hgefs",
]

weight_sums = result[weight_columns].sum(axis=1)

print("\nMaximum weight-sum error:")
print(abs(weight_sums - 1).max())