import requests
import pandas as pd

CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946)
}

START_DATE = "2025-01-01"
END_DATE = "2026-01-31"

all_weather = []

for city, (lat, lon) in CITIES.items():

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={START_DATE}&end_date={END_DATE}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m"

    response = requests.get(url)
    data = response.json()

    hourly = data["hourly"]

    for i in range(len(hourly["time"])):
        all_weather.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "timestamp": hourly["time"][i],
            "temperature": hourly["temperature_2m"][i],
            "humidity": hourly["relative_humidity_2m"][i],
            "wind_speed": hourly["wind_speed_10m"][i],
            "wind_direction": hourly["wind_direction_10m"][i]
        })

df = pd.DataFrame(all_weather)
df.to_csv("data/raw/weather_data.csv", index=False)

print("Weather data collected successfully.")