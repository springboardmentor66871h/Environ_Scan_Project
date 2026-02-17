import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, UTC

load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")

HEADERS = {"X-API-Key": API_KEY}

BASE_URL = "https://api.openaq.org/v2/latest"

CITIES = [
    "Delhi", "Bhopal", "Mumbai", "Kolkata", "Bengaluru",
    "Chennai", "Lucknow", "Hyderabad", "Kanpur",
    "Patna", "Varanasi", "Ahmedabad", "Pune", "Jaipur"
]

POLLUTANTS = ["pm25", "pm10", "no2", "co", "so2", "o3"]


def fetch_city_pollution(city):
    params = {
        "city": city,
        "country": "IN",
        "limit": 1000
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("API error:", response.status_code)
        return []

    results = response.json().get("results", [])
    records = []

    for location in results:
        coords = location.get("coordinates")
        if not coords:
            continue

        lat = coords.get("latitude")
        lon = coords.get("longitude")

        for measurement in location.get("measurements", []):
            if measurement["parameter"] not in POLLUTANTS:
                continue

            records.append({
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "timestamp": measurement["lastUpdated"],
                "pollutant": measurement["parameter"],
                "value": measurement["value"],
                "unit": measurement["unit"]
            })

    return records


def collect_all_data():
    dataset = []

    for city in CITIES:
        print(f"Collecting data for {city}...")
        data = fetch_city_pollution(city)
        print(f"{city} records:", len(data))
        dataset.extend(data)

    return pd.DataFrame(dataset)


if __name__ == "__main__":
    print("Starting OpenAQ data collection...")

    df = collect_all_data()

    if df.empty:
        print("No data collected.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.drop_duplicates()

        os.makedirs("data/raw", exist_ok=True)
        path = "data/raw/pollution_openaq.csv"
        df.to_csv(path, index=False)

        print("\nDataset saved:", path)
        print("Total records:", len(df))
