from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from evaluate_adaptive import get_temperature_performance
from evaluate_precipitation import get_precipitation_performance
from backend.ingestion.fetch_weather import fetch_all_models
from backend.forecast.forecast_engine import generate_hybrid_forecast
import time


app = FastAPI(
    title="Adaptive Weather Blending API",
    description="Hybrid AI-NWP weather forecasting API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


LATITUDE = 8.5241
LONGITUDE = 76.9366
LOCATION_NAME = "Thiruvananthapuram"

FORECAST_CACHE = None
FORECAST_CACHE_TIME = 0
CACHE_TTL = 600  # 10 minutes


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Adaptive Weather Blending API",
    }


@app.get("/forecast")
def get_forecast():
    global FORECAST_CACHE, FORECAST_CACHE_TIME

    now = time.time()

    # Return cached forecast if still valid
    if FORECAST_CACHE is not None and now - FORECAST_CACHE_TIME < CACHE_TTL:
        return FORECAST_CACHE

    # Fetch fresh data
    forecasts = fetch_all_models(
        LATITUDE,
        LONGITUDE,
    )

    result = generate_hybrid_forecast(
        forecasts,
        LATITUDE,
        LONGITUDE,
        LOCATION_NAME,
    )

    # Save to cache
    FORECAST_CACHE = result
    FORECAST_CACHE_TIME = now

    return result

@app.get("/performance")
def get_performance():

    return {
        "temperature": get_temperature_performance(),
        "precipitation": get_precipitation_performance(),
    }