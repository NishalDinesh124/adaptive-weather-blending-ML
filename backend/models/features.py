import pandas as pd


TEMP_FORECAST_COLUMNS = [
    "ifs_temp",
    "gfs_temp",
    "aifs_temp",
    "hgefs_temp",
]


TEMPERATURE_FEATURE_COLUMNS = [
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

PRECIP_FORECAST_COLUMNS = [
    "ifs_precip",
    "gfs_precip",
    "aifs_precip",
    "hgefs_precip",
]

PRECIPITATION_FEATURE_COLUMNS = [
    "hour",
    "month",
    "day_of_year",
    "ifs_precip",
    "gfs_precip",
    "aifs_precip",
    "hgefs_precip",
    "precip_mean",
    "precip_std",
    "precip_min",
    "precip_max",
]


def build_temperature_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build temperature features used by the adaptive error models.

    These features are available at forecast time, so this function
    does not depend on ERA5 or any other observation/reference data.
    """

    features = pd.DataFrame(index=df.index)

    # --------------------------------------------------
    # Time/context features
    # --------------------------------------------------

    time = pd.to_datetime(df["time"])

    features["hour"] = time.dt.hour
    features["month"] = time.dt.month
    features["day_of_year"] = time.dt.dayofyear

    # --------------------------------------------------
    # Forecasts from the four source models
    # --------------------------------------------------

    for column in TEMP_FORECAST_COLUMNS:
        features[column] = df[column]

    # --------------------------------------------------
    # Cross-model statistics
    # --------------------------------------------------

    forecasts = df[TEMP_FORECAST_COLUMNS]

    features["temp_mean"] = forecasts.mean(axis=1)
    features["temp_std"] = forecasts.std(axis=1)
    features["temp_min"] = forecasts.min(axis=1)
    features["temp_max"] = forecasts.max(axis=1)

    return features


def build_precipitation_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build precipitation features available at forecast time.
    Does not depend on ERA5 or any observation/reference data.
    """
    features = pd.DataFrame(index=df.index)

    time = pd.to_datetime(df["time"])

    features["hour"] = time.dt.hour
    features["month"] = time.dt.month
    features["day_of_year"] = time.dt.dayofyear

    for column in PRECIP_FORECAST_COLUMNS:
        features[column] = df[column]

    forecasts = df[PRECIP_FORECAST_COLUMNS]

    features["precip_mean"] = forecasts.mean(axis=1)
    features["precip_std"] = forecasts.std(axis=1)
    features["precip_min"] = forecasts.min(axis=1)
    features["precip_max"] = forecasts.max(axis=1)

    return features