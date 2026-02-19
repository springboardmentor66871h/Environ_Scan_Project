import os
import requests
import pandas as pd
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
#import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if API_KEY is None:
    raise ValueError("OPENWEATHER_API_KEY not set in environment variables")
BASE_PATH = r"D:\ENVIRON-SCAN"
RAW_PATH = os.path.join(BASE_PATH, "data", "raw")
os.makedirs(RAW_PATH, exist_ok=True)

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639)
}

start_date = int(datetime(2023, 11, 1).timestamp())
end_date = int(datetime(2024, 2, 29).timestamp())

all_data = []

# ==========================================
# DATA COLLECTION
# ==========================================

for city, (lat, lon) in cities.items():

    print(f"Collecting pollution data for {city}...")

    url = "https://api.openweathermap.org/data/2.5/air_pollution/history"

    params = {
        "lat": lat,
        "lon": lon,
        "start": start_date,
        "end": end_date,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching {city}: {response.json()}")
        continue

    data = response.json()

    for item in data["list"]:
        record = {
            "timestamp": datetime.utcfromtimestamp(item["dt"]),
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "pm25": item["components"]["pm2_5"],
            "pm10": item["components"]["pm10"],
            "co": item["components"]["co"],
            "no2": item["components"]["no2"],
            "so2": item["components"]["so2"],
            "o3": item["components"]["o3"]
        }
        all_data.append(record)

pollution_df = pd.DataFrame(all_data)

# Ensure datetime format clean
pollution_df["timestamp"] = pd.to_datetime(pollution_df["timestamp"])
pollution_df.sort_values(by=["city", "timestamp"], inplace=True)
pollution_df.reset_index(drop=True, inplace=True)

file_path = os.path.join(RAW_PATH, "pollution.csv")
pollution_df.to_csv(file_path, index=False)

print("\nPollution dataset saved.")
print("Total rows:", len(pollution_df))
