#backend/model/predict.py
from pathlib import Path

import numpy as np
import pandas as pd
from xgboost import XGBRegressor

from .features import (
    PRECIPITATION_FEATURE_COLUMNS,
    build_precipitation_features,
    build_temperature_features,
)


# ==================================================
# Configuration
# ==================================================

MODEL_NAMES = ["ifs", "gfs", "aifs", "hgefs"]

FORECAST_COLUMNS = {
    "ifs": "ifs_temp",
    "gfs": "gfs_temp",
    "aifs": "aifs_temp",
    "hgefs": "hgefs_temp",
}

FEATURE_COLUMNS = [
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

EPSILON = 1e-6

BASE_DIR = Path(__file__).resolve().parents[2]

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
# Load trained models
# ==================================================

def load_temperature_models():
    models = {}

    for model_name in MODEL_NAMES:
        model_path = MODEL_DIR / f"{model_name}_error.json"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Trained model not found: {model_path}"
            )

        model = XGBRegressor()
        model.load_model(model_path)

        models[model_name] = model

    return models


# ==================================================
# Generate adaptive temperature forecast
# ==================================================

def generate_adaptive_temperature_forecast(df: pd.DataFrame):
    """
    Generate a dynamic weighted temperature forecast.

    The trained XGBoost models predict the expected absolute
    error of each weather model.

    Lower predicted error -> higher weight.
    """

    models = load_temperature_models()

    # Build the exact same feature structure used during training.
    features = build_temperature_features(df)

    # MVP uses only the original non-rolling features.
    X = features[FEATURE_COLUMNS].copy()

    predicted_errors = {}

    for model_name in MODEL_NAMES:
        model = models[model_name]

        predicted_error = model.predict(X)

        # Error cannot meaningfully be negative.
        predicted_error = np.maximum(
            predicted_error,
            EPSILON,
        )

        predicted_errors[model_name] = predicted_error

    # --------------------------------------------------
    # Convert predicted errors -> reliability scores
    # --------------------------------------------------

    error_df = pd.DataFrame(
        predicted_errors,
        index=df.index,
    )

    score_df = 1.0 / (error_df + EPSILON)

    # Normalize scores so weights sum to 1.
    weight_df = score_df.div(
        score_df.sum(axis=1),
        axis=0,
    )

    # --------------------------------------------------
    # Weighted hybrid forecast
    # --------------------------------------------------

    hybrid_forecast = np.zeros(len(df))

    for model_name in MODEL_NAMES:
        forecast_column = FORECAST_COLUMNS[model_name]

        hybrid_forecast += (
            weight_df[model_name].to_numpy()
            * df[forecast_column].to_numpy()
        )

    # --------------------------------------------------
    # Build result
    # --------------------------------------------------

    result = df[
        ["time"] + list(FORECAST_COLUMNS.values())
    ].copy()

    result["predicted_error_ifs"] = error_df["ifs"]
    result["predicted_error_gfs"] = error_df["gfs"]
    result["predicted_error_aifs"] = error_df["aifs"]
    result["predicted_error_hgefs"] = error_df["hgefs"]

    result["weight_ifs"] = weight_df["ifs"]
    result["weight_gfs"] = weight_df["gfs"]
    result["weight_aifs"] = weight_df["aifs"]
    result["weight_hgefs"] = weight_df["hgefs"]

    result["hybrid_temp"] = hybrid_forecast

    return result

# ==================================================
# Load trained precipitation model
# ==================================================

def load_precipitation_model():
    model_path = (
        PRECIP_MODEL_DIR
        / "precipitation_tweedie.json"
    )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained precipitation model not found: {model_path}"
        )

    model = XGBRegressor()
    model.load_model(model_path)

    return model


# ==================================================
# Generate precipitation forecast
# ==================================================

def generate_precipitation_forecast(
    df: pd.DataFrame,
):
    """
    Generate a precipitation forecast using
    the trained XGBoost Tweedie model.
    """

    model = load_precipitation_model()

    # Build the exact same features used during training.
    features = build_precipitation_features(df)

    X = features[
        PRECIPITATION_FEATURE_COLUMNS
    ].copy()

    # Generate precipitation forecast.
    predictions = model.predict(X)

    # Physical precipitation cannot be negative.
    predictions = np.maximum(
        predictions,
        0.0,
    )

    # --------------------------------------------------
    # Build result
    # --------------------------------------------------

    result = df[
        [
            "time",
            "ifs_precip",
            "gfs_precip",
            "aifs_precip",
            "hgefs_precip",
        ]
    ].copy()

    result["hybrid_precip"] = predictions

    return result