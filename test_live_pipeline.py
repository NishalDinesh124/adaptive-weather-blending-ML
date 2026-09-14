from backend.ingestion.fetch_weather import (
    fetch_all_models,
)

from backend.forecast.forecast_engine import (
    generate_hybrid_forecast,
)


LATITUDE = 8.5241
LONGITUDE = 76.9366


def main():

    print("=" * 70)
    print("LIVE HYBRID FORECAST PIPELINE")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Fetch live forecasts
    # --------------------------------------------------

    print("\nFetching live forecasts...\n")

    forecasts = fetch_all_models(
        LATITUDE,
        LONGITUDE,
    )

    print(
        f"\nFetched {len(forecasts)} timestamps."
    )

    # --------------------------------------------------
    # 2. Run hybrid ML system
    # --------------------------------------------------

    print("\nRunning hybrid forecast engine...\n")

    result = generate_hybrid_forecast(
    forecasts,
    location_name="Thiruvananthapuram",
    latitude=LATITUDE,
    longitude=LONGITUDE,
)

    # --------------------------------------------------
    # 3. Display first forecast
    # --------------------------------------------------

    first = result["forecast"][0]

    print("=" * 70)
    print("FIRST HYBRID FORECAST")
    print("=" * 70)

    print(
        f"\nTime: {first['time']}"
    )

    print("\nTemperature:")

    print(
        f"  Hybrid: "
        f"{first['temperature']['hybrid']:.2f} °C"
    )

    print("\n  Model weights:")

    for model, weight in (
        first["temperature"]["weights"]
        .items()
    ):
        print(
            f"    {model.upper():<6}: "
            f"{weight:.3f}"
        )

    print("\nPrecipitation:")

    print(
        f"  Hybrid: "
        f"{first['precipitation']['hybrid']:.2f} mm"
    )

    print("\n  Source forecasts:")

    for model, value in (
        first["precipitation"]["sources"]
        .items()
    ):
        print(
            f"    {model.upper():<6}: "
            f"{value:.2f} mm"
        )


if __name__ == "__main__":
    main()