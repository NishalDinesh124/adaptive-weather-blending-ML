from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from evaluate_adaptive import get_temperature_performance
from evaluate_precipitation import get_precipitation_performance
from backend.ingestion.fetch_weather import fetch_all_models
from backend.forecast.forecast_engine import generate_hybrid_forecast


app = FastAPI(
    title="Adaptive Weather Blending API",
    description="Hybrid AI-NWP weather forecasting API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LATITUDE = 8.5241
LONGITUDE = 76.9366
LOCATION_NAME = "Thiruvananthapuram"


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Adaptive Weather Blending API",
    }


@app.get("/forecast")
def get_forecast():

    forecasts = fetch_all_models(
        LATITUDE,
        LONGITUDE,
    )

    result = generate_hybrid_forecast(
        forecasts,
        location_name=LOCATION_NAME,
        latitude=LATITUDE,
        longitude=LONGITUDE,
    )

    return result

@app.get("/performance")
def get_performance():

    return {
        "temperature": get_temperature_performance(),
        "precipitation": get_precipitation_performance(),
    }