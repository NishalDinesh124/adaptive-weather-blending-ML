#evaluate_adaptive.py
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from backend.models.predict import generate_adaptive_temperature_forecast


# ==================================================
# 1. Load data
# ==================================================

df = pd.read_csv(
    "data/processed/training_dataset.csv"
)

df["time"] = pd.to_datetime(df["time"])


# ==================================================
# 2. Chronological test split
# ==================================================

split_index = int(len(df) * 0.8)

test_df = df.iloc[split_index:].copy()


# ==================================================
# 3. Generate adaptive predictions
# ==================================================

result = generate_adaptive_temperature_forecast(test_df)


# ==================================================
# 4. Evaluation helper
# ==================================================

def evaluate(name, predictions):
    actual = test_df["era5_temp"]

    mae = mean_absolute_error(actual, predictions)

    rmse = mean_squared_error(
        actual,
        predictions,
    ) ** 0.5

    print(
        f"{name:<20} "
        f"MAE: {mae:.3f} | "
        f"RMSE: {rmse:.3f}"
    )


# ==================================================
# 5. Individual models
# ==================================================

print("\n" + "=" * 65)
print("TEMPERATURE FORECAST EVALUATION")
print("=" * 65)

evaluate(
    "IFS",
    test_df["ifs_temp"],
)

evaluate(
    "GFS",
    test_df["gfs_temp"],
)

evaluate(
    "AIFS",
    test_df["aifs_temp"],
)

evaluate(
    "HGEFS",
    test_df["hgefs_temp"],
)


# ==================================================
# 6. Equal-weight baseline
# ==================================================

equal_weight = (
    test_df["ifs_temp"]
    + test_df["gfs_temp"]
    + test_df["aifs_temp"]
    + test_df["hgefs_temp"]
) / 4

evaluate(
    "Equal-weight blend",
    equal_weight,
)


# ==================================================
# 7. Adaptive XGBoost blend
# ==================================================

evaluate(
    "Adaptive XGBoost",
    result["hybrid_temp"],
)


# ==================================================
# 8. Weight sanity check
# ==================================================

weights = result[
    [
        "weight_ifs",
        "weight_gfs",
        "weight_aifs",
        "weight_hgefs",
    ]
]

print("\nMaximum weight-sum error:")
print(abs(weights.sum(axis=1) - 1).max())