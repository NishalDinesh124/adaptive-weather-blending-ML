from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from .features import (
    PRECIPITATION_FEATURE_COLUMNS,
    TEMPERATURE_FEATURE_COLUMNS,
    build_precipitation_features,
    build_temperature_features,
)


# ==================================================
# Configuration
# ==================================================

MODEL_NAMES = [
    "ifs",
    "gfs",
    "aifs",
    "hgefs",
]


FORECAST_COLUMNS = {
    "ifs": "ifs_temp",
    "gfs": "gfs_temp",
    "aifs": "aifs_temp",
    "hgefs": "hgefs_temp",
}


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "training_dataset.csv"
)


MODEL_DIR = (
    BASE_DIR
    / "backend"
    / "models"
    / "saved"
    / "temperature"
)

PRECIP_MODEL_DIR = (
    BASE_DIR
    / "backend"
    / "models"
    / "saved"
    / "precipitation"
)

# ==================================================
# XGBoost configuration
# ==================================================

XGB_PARAMS = {
    "n_estimators": 300,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "random_state": 42,
}

PRECIP_XGB_PARAMS = {
    "n_estimators": 300,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:tweedie",
    "tweedie_variance_power": 1.4,
    "random_state": 42,
}


# ==================================================
# Data loading
# ==================================================

def load_training_data() -> pd.DataFrame:
    """Load and prepare the processed training dataset."""

    df = pd.read_csv(DATA_FILE)

    df["time"] = pd.to_datetime(df["time"])

    df = df.sort_values("time").reset_index(drop=True)

    return df


# ==================================================
# Chronological split
# ==================================================

def split_data(
    df: pd.DataFrame,
    train_fraction: float = 0.8,
):
    """
    Split data chronologically.

    Older observations are used for training and newer
    observations are reserved for testing.
    """

    split_index = int(len(df) * train_fraction)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    return train_df, test_df


# ==================================================
# Train one error model
# ==================================================

def train_error_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> XGBRegressor:

    model = XGBRegressor(**XGB_PARAMS)

    model.fit(X_train, y_train)

    return model


# ==================================================
# Evaluate one error model
# ==================================================

def evaluate_error_model(
    model: XGBRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
):
    """Evaluate how well the model predicts forecast error."""

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    return mae, rmse


# ==================================================
# Train all temperature error models
# ==================================================

def train_temperature_models():

    print("=" * 65)
    print("TEMPERATURE ERROR MODEL TRAINING")
    print("=" * 65)

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    df = load_training_data()

    # --------------------------------------------------
    # Build features
    # --------------------------------------------------

    features = build_temperature_features(df)

    X = features[TEMPERATURE_FEATURE_COLUMNS]

    # --------------------------------------------------
    # Chronological split
    # --------------------------------------------------

    train_df, test_df = split_data(df)

    train_indices = train_df.index
    test_indices = test_df.index

    X_train = X.loc[train_indices]
    X_test = X.loc[test_indices]

    print(f"\nTraining rows: {len(X_train)}")
    print(f"Testing rows:  {len(X_test)}")

    # --------------------------------------------------
    # Create model directory
    # --------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = {}

    # --------------------------------------------------
    # Train one model for each forecast source
    # --------------------------------------------------

    for model_name in MODEL_NAMES:

        forecast_column = FORECAST_COLUMNS[model_name]

        # Target = absolute forecast error
        y = (
            df[forecast_column]
            - df["era5_temp"]
        ).abs()

        y_train = y.loc[train_indices]
        y_test = y.loc[test_indices]

        print(
            f"\nTraining error model: "
            f"{model_name.upper()}"
        )

        model = train_error_model(
            X_train,
            y_train,
        )

        mae, rmse = evaluate_error_model(
            model,
            X_test,
            y_test,
        )

        model_file = (
            MODEL_DIR
            / f"{model_name}_error.json"
        )

        model.save_model(model_file)

        results[model_name] = {
            "mae": mae,
            "rmse": rmse,
        }

        print(
            f"Saved → {model_file}"
        )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\n")
    print("=" * 65)
    print("TEMPERATURE ERROR MODEL TRAINING")
    print("=" * 65)

    for model_name in MODEL_NAMES:

        result = results[model_name]

        print(
            f"{model_name.upper():<10} "
            f"MAE: {result['mae']:.3f} | "
            f"RMSE: {result['rmse']:.3f}"
        )

    print("\nModels saved to:")
    print(MODEL_DIR)


def train_precipitation_model():

    print("=" * 65)
    print("PRECIPITATION MODEL TRAINING")
    print("=" * 65)

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    df = load_training_data()

    # --------------------------------------------------
    # Build features
    # --------------------------------------------------

    features = build_precipitation_features(df)

    X = features[PRECIPITATION_FEATURE_COLUMNS]

    # --------------------------------------------------
    # Chronological split
    # --------------------------------------------------

    train_df, test_df = split_data(df)

    train_indices = train_df.index
    test_indices = test_df.index

    X_train = X.loc[train_indices]
    X_test = X.loc[test_indices]

    y = df["era5_precip"]

    y_train = y.loc[train_indices]
    y_test = y.loc[test_indices]

    print(f"\nTraining rows: {len(X_train)}")
    print(f"Testing rows:  {len(X_test)}")

    # --------------------------------------------------
    # Train model
    # --------------------------------------------------

    model = XGBRegressor(**PRECIP_XGB_PARAMS)

    print("\nTraining Tweedie precipitation model...")

    model.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------
    # Evaluate precipitation target prediction
    # --------------------------------------------------

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    PRECIP_MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_file = (
        PRECIP_MODEL_DIR
        / "precipitation_tweedie.json"
    )

    model.save_model(model_file)

    print(f"\nMAE:  {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Saved → {model_file}")

# ==================================================
# Entry point
# ==================================================

if __name__ == "__main__":
    train_temperature_models()
    train_precipitation_model()