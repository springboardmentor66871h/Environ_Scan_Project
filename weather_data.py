import os
import requests
import pandas as pd

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

start_date = "2023-11-01"
end_date = "2024-02-29"

all_weather = []

for city, (lat, lon) in cities.items():

    print(f"Collecting weather for {city}...")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "wind_direction_10m"
        ]
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error:", response.json())
        continue

    data = response.json()
    df = pd.DataFrame(data["hourly"])

    df["timestamp"] = pd.to_datetime(df["time"])
    df["city"] = city
    df["latitude"] = lat
    df["longitude"] = lon

    df.rename(columns={
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "wind_speed",
        "wind_direction_10m": "wind_direction"
    }, inplace=True)

    df = df.drop(columns=["time"])

    all_weather.append(df)

weather_df = pd.concat(all_weather, ignore_index=True)

weather_df.sort_values(by=["city", "timestamp"], inplace=True)
weather_df.reset_index(drop=True, inplace=True)

file_path = os.path.join(RAW_PATH, "weather.csv")
weather_df.to_csv(file_path, index=False)

print("\nWeather dataset saved.")
print("Total rows:", len(weather_df))
