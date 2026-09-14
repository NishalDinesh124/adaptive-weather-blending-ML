from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from backend.models.predict import generate_precipitation_forecast


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

MODEL_NAMES = [
    "ifs",
    "gfs",
    "aifs",
    "hgefs",
]

FORECAST_COLUMNS = {
    "ifs": "ifs_precip",
    "gfs": "gfs_precip",
    "aifs": "aifs_precip",
    "hgefs": "hgefs_precip",
}

# IMD-style hourly precipitation thresholds
RAIN_THRESHOLDS = [
    0.1,
    2.5,
    15.6,
]

def count_events(actual, predictions, threshold):
    print(f"\nEVENT COUNTS — >= {threshold} mm/h")
    print("-" * 65)

    actual_events = (actual >= threshold).sum()

    print(f"{'Model':<22} {'Predicted Events':>18}")
    print(f"{'Actual':<22} {actual_events:>18}")

    for name, pred in predictions.items():
        predicted_events = (pred >= threshold).sum()
        print(f"{name:<22} {predicted_events:>18}")


# ==================================================
# Data loading
# ==================================================

def load_data():
    df = pd.read_csv(DATA_FILE)

    df["time"] = pd.to_datetime(df["time"])

    df = (
        df
        .sort_values("time")
        .reset_index(drop=True)
    )

    return df


# ==================================================
# Chronological split
# ==================================================

def split_data(
    df: pd.DataFrame,
    train_fraction: float = 0.8,
):
    split_index = int(
        len(df) * train_fraction
    )

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    return train_df, test_df


# ============================================================
# CONTINUOUS METRICS
# ============================================================

# ... your existing MAE/RMSE evaluation here ...

def calculate_continuous_metrics(
    actual,
    predicted,
):
    mae = mean_absolute_error(
        actual,
        predicted,
    )

    rmse = mean_squared_error(
        actual,
        predicted,
    ) ** 0.5

    return mae, rmse


# ==================================================
# Contingency table
# ==================================================

def calculate_contingency_metrics(
    actual,
    predicted,
    threshold,
):
    actual_event = actual >= threshold
    predicted_event = predicted >= threshold

    hits = (
        actual_event
        & predicted_event
    ).sum()

    false_alarms = (
        ~actual_event
        & predicted_event
    ).sum()

    misses = (
        actual_event
        & ~predicted_event
    ).sum()

    correct_negatives = (
        ~actual_event
        & ~predicted_event
    ).sum()

    # Probability of Detection
    if hits + misses > 0:
        pod = hits / (hits + misses)
    else:
        pod = 0.0

    # False Alarm Ratio
    if hits + false_alarms > 0:
        far = false_alarms / (
            hits + false_alarms
        )
    else:
        far = 0.0

    # Critical Success Index
    if (
        hits
        + false_alarms
        + misses
        > 0
    ):
        csi = hits / (
            hits
            + false_alarms
            + misses
        )
    else:
        csi = 0.0

    # Equitable Threat Score
    total = (
        hits
        + false_alarms
        + misses
        + correct_negatives
    )

    random_hits = (
        (hits + false_alarms)
        * (hits + misses)
        / total
    )

    denominator = (
        hits
        + false_alarms
        + misses
        - random_hits
    )

    if denominator > 0:
        ets = (
            hits - random_hits
        ) / denominator
    else:
        ets = 0.0

    return {
        "pod": pod,
        "far": far,
        "csi": csi,
        "ets": ets,
        "hits": hits,
        "false_alarms": false_alarms,
        "misses": misses,
    }


# ==================================================
# Main evaluation
# ==================================================

def evaluate_precipitation():

    print("=" * 75)
    print("PRECIPITATION FORECAST EVALUATION")
    print("=" * 75)

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    df = load_data()

    train_df, test_df = split_data(df)

    print(f"\nTotal rows:     {len(df)}")
    print(f"Training rows:  {len(train_df)}")
    print(f"Testing rows:   {len(test_df)}")

    print(
        f"\nTest period: "
        f"{test_df['time'].iloc[0]} → "
        f"{test_df['time'].iloc[-1]}"
    )

    actual = test_df["era5_precip"]

    # --------------------------------------------------
    # Generate Tweedie predictions
    # --------------------------------------------------

    tweedie_result = (
        generate_precipitation_forecast(
            test_df
        )
    )

    predictions = {}

    # Raw model forecasts
    for model_name in MODEL_NAMES:
        predictions[model_name] = (
            test_df[
                FORECAST_COLUMNS[model_name]
            ].to_numpy()
        )

    # Equal-weight blend
    predictions["equal"] = (
        test_df[
            list(FORECAST_COLUMNS.values())
        ]
        .mean(axis=1)
        .to_numpy()
    )

    # Adaptive / ML forecast
    predictions["tweedie"] = (
        tweedie_result[
            "hybrid_precip"
        ].to_numpy()
    )

     # --------------------------------------------------
    # Event-count diagnostic
    # --------------------------------------------------

    count_events(
        actual.to_numpy(),
        predictions,
        0.1,
    )

    count_events(
        actual.to_numpy(),
        predictions,
        2.5,
    )

    # --------------------------------------------------
    # Continuous evaluation
    # --------------------------------------------------

    print("\n")
    print("-" * 75)
    print("CONTINUOUS METRICS")
    print("-" * 75)

    continuous_results = {}

    display_names = {
        "ifs": "IFS",
        "gfs": "GFS",
        "aifs": "AIFS",
        "hgefs": "HGEFS",
        "equal": "Equal-weight blend",
        "tweedie": "Tweedie XGBoost",
    }

    for model_name, predicted in predictions.items():

        mae, rmse = calculate_continuous_metrics(
            actual,
            predicted,
        )

        continuous_results[model_name] = {
            "mae": mae,
            "rmse": rmse,
        }

        print(
            f"{display_names[model_name]:<20}"
            f" MAE: {mae:.3f}"
            f" | RMSE: {rmse:.3f}"
        )

    # --------------------------------------------------
    # Event-based evaluation
    # --------------------------------------------------

    for threshold in RAIN_THRESHOLDS:

        print("\n")
        print("-" * 75)
        print(
            f"EVENT METRICS — "
            f"RAINFALL >= {threshold} mm/h"
        )
        print("-" * 75)

        print(
            f"{'Model':<20}"
            f"{'POD':>8}"
            f"{'FAR':>8}"
            f"{'CSI':>8}"
            f"{'ETS':>8}"
        )

        for model_name, predicted in predictions.items():

            metrics = calculate_contingency_metrics(
                actual.to_numpy(),
                predicted,
                threshold,
            )

            print(
                f"{display_names[model_name]:<20}"
                f"{metrics['pod']:>8.3f}"
                f"{metrics['far']:>8.3f}"
                f"{metrics['csi']:>8.3f}"
                f"{metrics['ets']:>8.3f}"
            )




# ==================================================
# Entry point
# ==================================================

if __name__ == "__main__":
    evaluate_precipitation()