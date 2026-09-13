import requests

LATITUDE = 8.5241
LONGITUDE = 76.9366

URL = "https://api.open-meteo.com/v1/ecmwf"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "precipitation,temperature_2m,wind_speed_10m",
    "forecast_days": 3,
    "timezone": "Asia/Kolkata",
}

response = requests.get(URL, params=params, timeout=30)

response.raise_for_status()

data = response.json()

print("Location:", data["latitude"], data["longitude"])
print("Model: ECMWF")
print()
print("First 5 forecast hours:")

for i in range(5):
    print(
        data["hourly"]["time"][i],
        "Rain:", data["hourly"]["precipitation"][i], "mm",
        "Temp:", data["hourly"]["temperature_2m"][i], "°C",
        "Wind:", data["hourly"]["wind_speed_10m"][i], "km/h",
    )