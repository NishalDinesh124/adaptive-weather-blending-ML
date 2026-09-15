#backend/forecast/forecast_engine.py
import pandas as pd

from backend.models.predict import (
    generate_adaptive_temperature_forecast,
    generate_precipitation_forecast,
)


# ==================================================
# Prototype location
# ==================================================



# ==================================================
# Generate complete hybrid forecast
# ==================================================

def generate_hybrid_forecast(
    forecasts: pd.DataFrame,
    location_name: str,
    latitude: float,
    longitude: float,
):
    """
    Generate the complete hybrid forecast from
    live forecasts produced by the four source models.

    Temperature:
        Adaptive XGBoost error-based blending.

    Precipitation:
        XGBoost Tweedie model.
    """

    # --------------------------------------------------
    # Generate temperature forecast
    # --------------------------------------------------

    temperature_result = (
        generate_adaptive_temperature_forecast(
            forecasts
        )
    )

    # --------------------------------------------------
    # Generate precipitation forecast
    # --------------------------------------------------

    precipitation_result = (
        generate_precipitation_forecast(
            forecasts
        )
    )

    # --------------------------------------------------
    # Build structured forecast output
    # --------------------------------------------------

    forecast_output = []

    for i in range(len(forecasts)):

        temperature = {
            "hybrid": float(
                temperature_result[
                    "hybrid_temp"
                ].iloc[i]
            ),

            "sources": {
                "ifs": float(
                    temperature_result[
                        "ifs_temp"
                    ].iloc[i]
                ),

                "gfs": float(
                    temperature_result[
                        "gfs_temp"
                    ].iloc[i]
                ),

                "aifs": float(
                    temperature_result[
                        "aifs_temp"
                    ].iloc[i]
                ),

                "hgefs": float(
                    temperature_result[
                        "hgefs_temp"
                    ].iloc[i]
                ),
            },

            "weights": {
                "ifs": float(
                    temperature_result[
                        "weight_ifs"
                    ].iloc[i]
                ),

                "gfs": float(
                    temperature_result[
                        "weight_gfs"
                    ].iloc[i]
                ),

                "aifs": float(
                    temperature_result[
                        "weight_aifs"
                    ].iloc[i]
                ),

                "hgefs": float(
                    temperature_result[
                        "weight_hgefs"
                    ].iloc[i]
                ),
            },

            "predicted_errors": {
                "ifs": float(
                    temperature_result[
                        "predicted_error_ifs"
                    ].iloc[i]
                ),

                "gfs": float(
                    temperature_result[
                        "predicted_error_gfs"
                    ].iloc[i]
                ),

                "aifs": float(
                    temperature_result[
                        "predicted_error_aifs"
                    ].iloc[i]
                ),

                "hgefs": float(
                    temperature_result[
                        "predicted_error_hgefs"
                    ].iloc[i]
                ),
            },
        }

        precipitation = {
            "hybrid": float(
                precipitation_result[
                    "hybrid_precip"
                ].iloc[i]
            ),

            "sources": {
                "ifs": float(
                    precipitation_result[
                        "ifs_precip"
                    ].iloc[i]
                ),

                "gfs": float(
                    precipitation_result[
                        "gfs_precip"
                    ].iloc[i]
                ),

                "aifs": float(
                    precipitation_result[
                        "aifs_precip"
                    ].iloc[i]
                ),

                "hgefs": float(
                    precipitation_result[
                        "hgefs_precip"
                    ].iloc[i]
                ),
            },
        }
        wind = {
            "sources": {
                "ifs": float(
                    forecasts["ifs_wind"].iloc[i]
                ),

                "gfs": float(
                    forecasts["gfs_wind"].iloc[i]
                ),

                "aifs": float(
                    forecasts["aifs_wind"].iloc[i]
                ),

                "hgefs": float(
                    forecasts["hgefs_wind"].iloc[i]
                ),
            },

            "maximum": float(
                max(
                    forecasts["ifs_wind"].iloc[i],
                    forecasts["gfs_wind"].iloc[i],
                    forecasts["aifs_wind"].iloc[i],
                    forecasts["hgefs_wind"].iloc[i],
                )
            ),
        }

        forecast_output.append({
            "time": str(
                forecasts["time"].iloc[i]
            ),

            "temperature": temperature,

            "precipitation": precipitation,

            "wind": wind,
        })

    # --------------------------------------------------
    # Final response
    # --------------------------------------------------

    return {
        "location": {
    "name": location_name,
    "latitude": latitude,
    "longitude": longitude,
},

        "forecast": forecast_output,
    }