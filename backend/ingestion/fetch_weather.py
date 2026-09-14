import requests
import pandas as pd


# ==================================================
# Configuration
# ==================================================

MODEL_CONFIGS = {
    "ifs": {
        "url": "https://api.open-meteo.com/v1/ecmwf",
    },
    "gfs": {
        "url": "https://api.open-meteo.com/v1/gfs",
    },
    "aifs": {
        "url": "https://api.open-meteo.com/v1/ecmwf",
        "params": {
            "models": "ecmwf_aifs025_single",
        },
    },
    "hgefs": {
        "url": "https://api.open-meteo.com/v1/gfs",
        "params": {
            "models": "ncep_hgefs025_ensemble_mean",
        },
    },
}


# ==================================================
# Fetch one model
# ==================================================

def fetch_model_forecast(
    model_name: str,
    latitude: float,
    longitude: float,
):
    """
    Fetch forecast data for one model from Open-Meteo.
    """

    config = MODEL_CONFIGS[model_name]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "precipitation,"
            "temperature_2m,"
            "wind_speed_10m"
        ),
        "forecast_days": 3,
        "timezone": "Asia/Kolkata",
    }

    # Add model-specific parameters
    params.update(config.get("params", {}))

    # --------------------------------------------------
    # API request
    # --------------------------------------------------

    try:
        response = requests.get(
            config["url"],
            params=params,
            timeout=30,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Failed to fetch {model_name.upper()} forecast: {exc}"
        ) from exc

    # --------------------------------------------------
    # Parse response
    # --------------------------------------------------

    data = response.json()

    if "hourly" not in data:
        raise RuntimeError(
            f"{model_name.upper()} response does not contain "
            "hourly forecast data."
        )

    hourly = data["hourly"]

    # --------------------------------------------------
    # Validate required fields
    # --------------------------------------------------

    required_fields = [
        "time",
        "precipitation",
        "temperature_2m",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in hourly
    ]

    if missing_fields:
        raise RuntimeError(
            f"{model_name.upper()} response is missing "
            f"fields: {missing_fields}"
        )

    # --------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------

    return pd.DataFrame({
        "time": hourly["time"],
        f"{model_name}_precip": hourly["precipitation"],
        f"{model_name}_temp": hourly["temperature_2m"],
        f"{model_name}_wind": hourly["wind_speed_10m"],
    })


# ==================================================
# Fetch all four models
# ==================================================

def fetch_all_models(
    latitude: float,
    longitude: float,
):
    """
    Fetch forecasts from all four forecasting systems
    and align them on common hourly timestamps.
    """

    model_data = []

    for model_name in MODEL_CONFIGS:

        print(f"Fetching {model_name.upper()}...")

        df = fetch_model_forecast(
            model_name,
            latitude,
            longitude,
        )

        model_data.append(df)

    # --------------------------------------------------
    # Merge all models on time
    # --------------------------------------------------

    combined = model_data[0]

    for df in model_data[1:]:
        combined = combined.merge(
            df,
            on="time",
            how="inner",
        )

    # --------------------------------------------------
    # Validate combined data
    # --------------------------------------------------

    if combined.empty:
        raise RuntimeError(
            "No common timestamps were available across all models."
        )

    if combined.isna().any().any():
        raise RuntimeError(
            "Combined forecast contains missing values."
        )

    # --------------------------------------------------
    # Sort by time
    # --------------------------------------------------

    combined["time"] = pd.to_datetime(
        combined["time"]
    )

    combined = (
        combined
        .sort_values("time")
        .reset_index(drop=True)
    )

    return combined


# ==================================================
# Quick test
# ==================================================

if __name__ == "__main__":

    LATITUDE = 8.5241
    LONGITUDE = 76.9366

    forecast = fetch_all_models(
        LATITUDE,
        LONGITUDE,
    )

    print("\n")
    print("=" * 70)
    print("LIVE FORECAST DATA")
    print("=" * 70)

    print(f"\nRows: {len(forecast)}")

    print(
        f"Time range: "
        f"{forecast['time'].iloc[0]} → "
        f"{forecast['time'].iloc[-1]}"
    )

    print("\nColumns:")
    print(forecast.columns.tolist())

    print("\nFirst 5 rows:")
    print(
        forecast.head().to_string(
            index=False
        )
    )