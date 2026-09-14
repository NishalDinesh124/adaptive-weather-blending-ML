from pathlib import Path

import pandas as pd

from backend.models.predict import (
    generate_adaptive_temperature_forecast,
)


# ==================================================
# Configuration
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "training_dataset.csv"
)


# ==================================================
# Load data
# ==================================================

df = pd.read_csv(DATA_FILE)

df["time"] = pd.to_datetime(df["time"])

df = (
    df
    .sort_values("time")
    .reset_index(drop=True)
)


# ==================================================
# Chronological test split
# ==================================================

split_index = int(len(df) * 0.8)

test_df = df.iloc[split_index:].copy()


print("=" * 70)
print("TEMPERATURE WEIGHT DIAGNOSTIC")
print("=" * 70)

print(f"\nTest rows: {len(test_df)}")

print(
    f"Test period: "
    f"{test_df['time'].iloc[0]} → "
    f"{test_df['time'].iloc[-1]}"
)


# ==================================================
# Generate adaptive forecast
# ==================================================

result = generate_adaptive_temperature_forecast(
    test_df
)


# ==================================================
# Weight statistics
# ==================================================

weight_columns = [
    "weight_ifs",
    "weight_gfs",
    "weight_aifs",
    "weight_hgefs",
]

print("\n")
print("-" * 70)
print("AVERAGE WEIGHTS")
print("-" * 70)

for column in weight_columns:

    print(
        f"{column:<20}"
        f" {result[column].mean():.3f}"
    )


# ==================================================
# Weight ranges
# ==================================================

print("\n")
print("-" * 70)
print("WEIGHT RANGES")
print("-" * 70)

for column in weight_columns:

    print(
        f"{column:<20}"
        f" min: {result[column].min():.3f}"
        f" | max: {result[column].max():.3f}"
    )


# ==================================================
# Dominant model frequency
# ==================================================

weights = result[weight_columns]

dominant_model = weights.idxmax(axis=1)

print("\n")
print("-" * 70)
print("DOMINANT MODEL FREQUENCY")
print("-" * 70)

counts = dominant_model.value_counts()

for model, count in counts.items():

    percentage = (
        count / len(result) * 100
    )

    print(
        f"{model:<20}"
        f" {count:>5} rows"
        f" ({percentage:>5.1f}%)"
    )


# ==================================================
# High-confidence dominance
# ==================================================

print("\n")
print("-" * 70)
print("HIGH-CONFIDENCE DOMINANCE")
print("-" * 70)

for threshold in [0.50, 0.75, 0.90]:

    print(
        f"\nWeight >= {threshold:.2f}:"
    )

    for column in weight_columns:

        count = (
            result[column] >= threshold
        ).sum()

        percentage = (
            count / len(result) * 100
        )

        print(
            f"  {column:<18}"
            f" {count:>5} rows"
            f" ({percentage:>5.1f}%)"
        )
        