import requests
import pandas as pd
from datetime import datetime

CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946)
}

START_DATE = "2025-01-01"
END_DATE = "2026-01-31"

all_data = []

for city, (lat, lon) in CITIES.items():

    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&start_date={START_DATE}&end_date={END_DATE}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"

    response = requests.get(url)
    data = response.json()

    hourly = data["hourly"]

    for i in range(len(hourly["time"])):
        all_data.append({
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "timestamp": hourly["time"][i],
            "pm10": hourly["pm10"][i],
            "pm2_5": hourly["pm2_5"][i],
            "co": hourly["carbon_monoxide"][i],
            "no2": hourly["nitrogen_dioxide"][i],
            "so2": hourly["sulphur_dioxide"][i],
            "o3": hourly["ozone"][i]
        })

df = pd.DataFrame(all_data)
df.to_csv("data/raw/pollution_data.csv", index=False)

print("Pollution data collected successfully.")